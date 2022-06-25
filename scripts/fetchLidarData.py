import geopandas as gpd
import os
import pdal
import json
from boundary import Boundaries
from shapely.geometry import Polygon, Point
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))
from log import App_Logger

app_logger = App_Logger("logs/fetchLidarData.log").get_app_logger()

class Lidar_Data_Fetch:
   
    def __init__(self, public_data_url="https://s3-us-west-2.amazonaws.com/usgs-lidar-public/", epsg=26915, fetch_json_path="../data/pipeline.json") -> None:
        """This method is used to instantiate the class

        Args:
            public_data_url (str): The publc url where the cloud point data is located. Defaults to "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
            epsg (int, optional): The coordinate reference system (epsg value, i.e refer to https://epsg.io/) used by the user. Defaults to 26915 (NAD83 / UTM zone 15N).
            fetch_json_path (str, optional): a template pdal pipeline description in the form of JSON. Defaults to "./fetch.json".
        """
        self.public_data_url = public_data_url
        self.fetch_json_path = fetch_json_path
        self.input_epsg = 3857
        self.output_epsg = epsg
        # todo if folder not exist create folder structure
        self.out_put_laz_path = "../data/laz/temp.laz"
        self.out_put_tif_path = "../data/tif/temp.tif"
        self.logger = App_Logger(
            "logs/fetchLidarData.log").get_app_logger()

    def readFetchJson(self, path: str) -> dict:
        """This method reads json file using python json lib.
        Args:
            path (str): path for the json file
        Returns:
            dict: a dictionary object of the parsed json file
        """
        try:
            with open(path, 'r') as json_file:
                dict_obj = json.load(json_file)
            self.logger.info(f"Reading Fetched Json: {path}")
            return dict_obj
        except FileNotFoundError as e:
            print(e)

    def get_polygon_boundaries(self, polygon: Polygon) -> tuple:
        """This method is used to calculate rectangular bounds of a given polygon and returns a string representation of the calculated bounds in a '({[minx, maxx]},{[miny,maxy]})' format (i.e the format our pdal pipeline's reader.ept (https://pdal.io/stages/readers.ept.html#readers-ept) expects. example ([-8242669, -8242529], [4966549, 4966674])).
        It also returns a string format of the given polygon in a format that pdal pipeline's  filters.crop opreation expects. i.e POLYGON((0 0, 5000 10000, 10000 0, 0 0))

        Args:
            polygon (Polygon): a given shapely.geometry.Polygon object

        Returns:
            tuple: returns a 2 element tuple in which the first is  a string representation of the calculated bounds in a '({[minx, maxx]},{[miny,maxy]})' format and the second is a string format of the given polygon in a format that pdal pipeline's  filters.crop opreation expects. i.e POLYGON((0 0, 5000 10000, 10000 0, 0 0))
        """
        polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
        polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.input_epsg)
        minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds
        polygon_input = 'POLYGON(('
        xcord, ycord = polygon_df['geometry'][0].exterior.coords.xy
        for x, y in zip(list(xcord), list(ycord)):
            polygon_input += f'{x} {y}, '
        polygon_input = polygon_input[:-2]
        polygon_input += '))'
        self.logger.info(f"Getting polygon boundary: {polygon}")
        return f"({[minx, maxx]},{[miny,maxy]})", polygon_input

    def getPipeline(self, region: str, polygon: Polygon):
        """This method prepares our fetching pipeline using by using pipeline json description found in the root directory of the package. 

        Args:
            region (str): the region defines the region  point cloud data resource. 
            polygon (Polygon): the polygon  is a shapely.geometry.Polygon object which defines the boundaries of our cloud data points to be fetched

        Returns:
            pdal.Pipeline: returns a prepared pdal pipeline object
        """

        fetch_json = self.readFetchJson(self.fetch_json_path)
        boundaries, polygon_input = self.get_polygon_boundaries(polygon)
        full_dataset_path = "http://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_FullState/ept.json"
        # full_dataset_path = f"{self.public_data_url}{region}/ept.json"

        # fetch_json['pipeline'][0]['filename'] = full_dataset_path
        fetch_json['pipeline'][0]['bounds'] = boundaries
        fetch_json['pipeline'][1]['polygon'] = polygon_input
        fetch_json['pipeline'][6]['out_srs'] = f'EPSG:{self.output_epsg}'

        pipeline = pdal.Pipeline(json.dumps(fetch_json))
        self.logger.info(f"Getting pipeline with: {region} and {polygon}")
        return pipeline

    def runPipeline(self, region: str, polygon: Polygon):
        """reads the point cloud data from the EPT resource on AWS. We give it a region and a boundary polygon.

        Args:
            region (str): region of the cloud data EPT resource 
            polygon (Polygon): a shapely.geometry.Polygon object which defines the boundaries of our cloud data points to be fetched.

        Returns:
            list: it returns a list of a numpy array of cloud point data 
        """
        pipeline = self.getPipeline(region, polygon)

        try:
            pipeline.execute()
            metadata = pipeline.metadata
            log = pipeline.log
            self.logger.info(f"Run pipeline from: {region}")
            return pipeline.arrays, self.output_epsg
        except RuntimeError as e:
            print(e)
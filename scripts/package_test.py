import pdal
import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point, mapping
import numpy as np
from pyproj import Proj, transform
import folium
import laspy as lp
import os, sys
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))
from log import App_Logger

app_logger = App_Logger("../logs/package_test.log").get_app_logger()

class test:
    def __init__(self):
        
        self.coordinates = [
        [-93.756055, 41.918115],
        [-93.756155, 41.918215],
        [-93.756396, 41.918475],
        [-93.755955, 41.918300],
        [-93.755795, 41.918000],
    ]
        self.logger = App_Logger(
            "../logs/package_test.log").get_app_logger()
    # loading json file
    def read_json(self, json_path):
        try:
            with open(json_path) as js:
                json_obj = json.load(js)
                self.logger.info(f"Reading Fetched Json: {json_path}")
            return json_obj

        except FileNotFoundError:
            print('File not found.')
            
    def convert_EPSG(self, fromT, lon, lat):
        P3857 = Proj(init='epsg:3857')
        P4326 = Proj(init='epsg:4326')
        if(fromT == 4326):
            input1 = P4326
            input2 = P3857
        else:
            input1= p3857
            input2= p4326
            
        x, y = transform(input1,input2, lon, lat)
        self.logger.info(f"Transform EPSG: {x}, {y}")
        return [x, y]
    
    def loop_EPSG_converter(self, listin):
        converted = []
        for item in listin:
            converted.append(self.convert_EPSG(4326, item[0], item[1]))
            self.logger.info(f"Map EPSG: {converted}")
        return converted
    
    def generate_polygon(self, coor, epsg):
        polygon_g = Polygon(coor)
        crs = {'init': 'epsg:'+str(epsg)}
        polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_g])   
        self.logger.info(f"Generate Polygon: {polygon}")    
        return polygon
    
    def generate_geo_df(self, pipe, epsg):
        try:
            cloud_points = []
            elevations =[]
            geometry_points=[]
            for row in pipe.arrays[0]:
                lst = row.tolist()[-3:]
                cloud_points.append(lst)
                elevations.append(lst[2])
                point = Point(lst[0], lst[1])
                geometry_points.append(point)
            geodf = gpd.GeoDataFrame(columns=["elevation", "geometry"])
            geodf['elevation'] = elevations
            geodf['geometry'] = geometry_points
            geodf = geodf.set_geometry("geometry")
            geodf.set_crs(epsg = epsg, inplace=True)
            self.logger.info(f"Geo dataframe generated")
            return geodf
        except RuntimeError as e:
            self.logger.info('fails to extract geo data frame')
            print(e)
            
    def show_on_map(self, polygon, zoom, polygon2):
        #region selection
        poly = mapping((polygon2.iloc[:,0][0]))
        tmp = poly['coordinates'][0][0]
        anchor = [tmp[1], tmp[0]]
        m = folium.Map(anchor,zoom_start=zoom, tiles='cartodbpositron')
        folium.GeoJson(polygon).add_to(m)
        folium.LatLngPopup().add_to(m)
        self.logger.info('fails to extract geo data frame')
        return m
    
    def modify_pipe_json(self, json_loc, url, region, in_epsg, out_epsg, polygon):
        dicti = self.read_json(json_loc)
        dicti['pipeline'][0]['polygon'] = str(polygon.iloc[:,0][0])
        dicti['pipeline'][0]['filename'] = f"{url}/{region}/ept.json"
        dicti['pipeline'][2]['in_srs'] = f"EPSG:{in_epsg}"
        dicti['pipeline'][2]['out_srs'] = f"EPSG:{out_epsg}"
        print(dicti)
        self.logger.info('json pipeline extraction')
        return dicti
    
    def plot_heatmap(self, df, title) -> None:
        """ Plots a 2D heat map for the point cloud data using matplotlib
        """

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        df.plot(column='elevation', ax=ax, legend=True, cmap="terrain")
        plt.title(title)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig('Heatmap.png', dpi=120)
        plt.show()
        self.logger.info('terrain heatmap plotted')
        
    def get_3D_visualzation(self, df, s=0.01, color="blue"):
    
        x = df.geometry.x
        y = df.geometry.y
        z = df.elevation

        points = np.vstack((x, y, z)).transpose()

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = plt.axes(projection='3d')
        ax.scatter(points[:, 0], points[:, 1],
                   points[:, 2],  s=0.01, color="blue")
        self.logger.info('3D visualization plotted')
        plt.show()
        
    def get_heatmap_visulazation(self, df: gpd.GeoDataFrame, cmap="terrain") -> None:
      
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        df.plot(column='elevation', ax=ax, legend=True, cmap=cmap)
        plt.show()
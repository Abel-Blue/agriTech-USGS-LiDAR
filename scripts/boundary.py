
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))
from log import App_Logger

app_logger = App_Logger("../logs/boundary.log").get_app_logger()

class Boundaries:
    """A class represntation of a rectangular bound
    """

    def __init__(self, ymin: float, xmin: float, ymax: float, xmax: float) -> None:
       
        self.ymin = ymin
        self.xmin = xmin
        self.ymax = ymax
        self.xmax = xmax
        self.logger = App_Logger(
            "../logs/boundary.log").get_app_logger()
        pass

    def getBounds(self) -> tuple:
        """Returns the extreme points defining the rectangular bounds in a list in the order of xmin, ymin, ymax, xmax
        """
        self.logger.info(f"get bounds: {self.xmin}, {self.ymin}  {self.ymax, self.xmax}")
        return ([self.xmin, self.ymin], [self.ymax, self.xmax])

    def getBoundStr(self) -> str:
        """Return a string representation of the extreme points defining the rectangular bounds in a '({[minx, maxx]},{[miny,maxy]})' format (i.e the format our pdal pipeline's reader.ept (https://pdal.io/stages/readers.ept.html#readers-ept) expects
        """
        self.logger.info(f"get bounds string: {self.xmin}, {self.xmax} {self.ymin}, {self.ymax}")
        return f"({[self.xmin, self.xmax]},{[self.ymin, self.ymax]})"
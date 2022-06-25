
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))
from log import App_Logger

app_logger = App_Logger("logs/boundary.log").get_app_logger()

class Boundaries:
   
    def __init__(self, ymin: float, xmin: float, ymax: float, xmax: float) -> None:
       
        self.ymin = ymin
        self.xmin = xmin
        self.ymax = ymax
        self.xmax = xmax
        self.logger = App_Logger(
            "logs/boundary.log").get_app_logger()
        pass

    def getBounds(self) -> tuple:
        self.logger.info(f"get bounds: {self.xmin}, {self.ymin}  {self.ymax, self.xmax}")
        return ([self.xmin, self.ymin], [self.ymax, self.xmax])

    def getBoundStr(self) -> str:
        self.logger.info(f"get bounds string: {self.xmin}, {self.xmax} {self.ymin}, {self.ymax}")
        return f"({[self.xmin, self.xmax]},{[self.ymin, self.ymax]})"
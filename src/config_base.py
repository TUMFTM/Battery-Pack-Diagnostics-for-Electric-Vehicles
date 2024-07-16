import os
import enum

class GeneralConfig(enum.Enum):
    """
    Holds the general config values for the VCA Paper
    """
        path2data = os.path.join(os.getcwd().partition('Code')[0], "Code","data")
    path2font = os.path.join(path2data, "font")
    
    path2figures = os.path.join(path2data,  "figures")
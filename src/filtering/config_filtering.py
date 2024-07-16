import enum


class FilteringConfig(enum.Enum):
    """
    Holds the general config values for the filtering steps
    """

    savgol_dict = {"polyorder": 2,
                   "deriv": 0,
                   "delta": 1.0,
                   "axis": -1,
                   "mode": "nearest",
                   "cval": 0.0}

    mean_dict = {"min_periods": 1,
                 "center" : False}

    butter_dict = {"btype": "low",
                   "analog": False}

    gaussian_dict = {"min_periods": 1,
                     "center" : False}
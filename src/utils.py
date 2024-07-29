# utils.py
import json
from datetime import timedelta
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def format_timestamp(seconds):
    # Convert seconds to timedelta and format as HH:MM:SS (rounded to the nearest second)
    td = timedelta(seconds=int(round(seconds)))
    return str(td)

import os
import json
import pandas as pd


def read_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        raise Exception("File does not exists.")


def load_attr_types(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise Exception("Missing attribute category info.")

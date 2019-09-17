import os
import json
import pandas as pd


def read_csv(path):
    if os.path.exists(path):
        df = pd.read_csv(path)
        if 'Class' in df.columns:
            df = df.rename(columns={'Class': 'class'})
        elif 'CLASS' in df.columns:
            df = df.rename(columns={'CLASS': 'class'})

        if 'class' not in df.columns:
            raise Exception("Dataset does not contains \"Class\" column.")

        return df
    else:
        raise Exception("File does not exists.")


def load_attr_types(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise Exception("Missing attribute category info.")

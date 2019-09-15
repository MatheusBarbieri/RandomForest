import os
import pandas as pd


def read_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        raise Exception("File does not exists.")


def get_attributes_names(df):
    return df.columns.to_list()

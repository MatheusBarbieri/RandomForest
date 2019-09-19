from math import log2
from util import group_by_attribute


def info(df):
    total = len(df)
    class_counts = df['class'].value_counts().to_list()
    total_info = 0

    for c in class_counts:
        x = c / total
        total_info = total_info - x * log2(x)

    return total_info


def info_attribute(attribute, df):
    instances_by_attribute = group_by_attribute(attribute, df)
    df_size = len(df)
    total_info = 0

    for _, group in instances_by_attribute:
        group_size = len(group)
        total_info = total_info + group_size / df_size * info(group)

    return total_info


def gain(attr, df):
    return info(df) - info_attribute(attr, df)

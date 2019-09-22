from numba import jit
import numpy as np


@jit(nopython=True)
def np_info(counts, size):
    total_info = 0
    for c in counts:
        x = c / size
        total_info = total_info - x * np.log2(x)

    return total_info


def info_attributes_calc(data, attributes, column_index):
    class_pos = column_index['class']
    total_size = len(data)

    infos = []
    for attr, kind in attributes:
        if kind == "nominal":
            unique = np.unique(data[:, column_index[attr]])
            groups = [data[data[:, column_index[attr]] == u] for u in unique]
        else:
            mean = data[:, column_index[attr]].mean()
            groups = [data[data[:, column_index[attr]] <= mean], data[data[:, column_index[attr]] > mean]]

        attr_info = 0
        for group in groups:
            group_size = len(group)
            class_column = group[:, class_pos]
            classes, counts = np.unique(class_column, return_counts=True)
            attr_info = attr_info + group_size / total_size * np_info(counts, group_size)

        infos.append(attr_info)
    return infos


def info_attributes(df, attributes):
    column_index = {v: i for i, v in enumerate(df.columns.values)}
    data = df.values
    return info_attributes_calc(data, attributes, column_index)


def attributes_gains(df, attributes):
    size = len(df)
    counts = df['class'].value_counts().to_numpy()
    df_info = np_info(counts, size)
    attr_infos = info_attributes(df, attributes)
    return [df_info - info for info in attr_infos]

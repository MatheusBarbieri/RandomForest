from numba import jit
import numpy as np


def _group_by_attribute(data, attributes_index, attribute, kind):
    if kind == "nominal":
        partition_index = np.unique(data[:, attributes_index[attribute]])
        groups = [data[data[:, attributes_index[attribute]] == i] for i in partition_index]
        return groups, partition_index
    else:
        column = data[:, attributes_index[attribute]]
        mean = column.mean()
        greater_than = data[data[:, attributes_index[attribute]] <= mean]
        lower_than = data[data[:, attributes_index[attribute]] > mean]

        if not lower_than.any():
            return [greater_than], [False]
        else:
            return [greater_than, lower_than], [False, True]


@jit(nopython=True)
def np_info(class_occurences, total_occurences):
    total_info = 0
    for occurence in class_occurences:
        probability = occurence / total_occurences
        total_info = total_info - probability * np.log2(probability)

    return total_info


def info_attributes(data, attributes_index, attributes_kinds, attributes_list, class_index):
    total_size = data.shape[0]
    infos, all_groups, all_groups_index = [], [], []

    for attr, kind in attributes_list:
        groups, groups_index = _group_by_attribute(data, attributes_index, attr, kind)

        attr_info = 0
        for group in groups:
            group_size = len(group)
            class_column = group[:, class_index]
            classes, counts = np.unique(class_column, return_counts=True)
            attr_info = attr_info + group_size / total_size * np_info(counts, group_size)

        infos.append(attr_info)
        all_groups.append(groups)
        all_groups_index.append(groups_index)

    return infos, all_groups, all_groups_index


def attributes_gains(data, attributes_index, attributes_kinds, attributes_list, class_index):
    total_size = data.shape[0]
    classes, counts = np.unique(class_index, return_counts=True)
    df_info = np_info(counts, total_size)
    attr_infos = info_attributes(data, attributes_index, attributes_kinds, attributes_list, class_index)
    return [df_info - info for info in attr_infos]

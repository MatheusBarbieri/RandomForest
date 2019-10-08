import random
import numpy as np
from information import info_attributes
from .print import tree_to_string


class Tree:
    def __init__(self, options=None, target_class=None, attribute=None, kind=None, cut=None):
        self.target_class = target_class
        self.options = options
        self.attribute = attribute
        self.kind = kind
        self.cut = cut

    def __str__(self):
        return tree_to_string(self)

    @classmethod
    def generate(cls, df, attributes_kinds, m=None):
        attributes_index = {v: i for i, v in enumerate(df.columns.values)}
        class_index = attributes_index.pop('class')
        data = df.values
        return _generate(data, attributes_index, attributes_kinds, class_index, m)


def _most_frequent_class(class_array):
    values, counts = np.unique(class_array, return_counts=True)
    return values[counts.argmax()]


def _is_class_unique(data, index):
    return np.unique(data[:, index]).size == 1


def _take_m(attributes, m):
    attribute_list = list(attributes.items())
    if m and len(attribute_list) >= m:
        attribute_list = random.sample(attribute_list, m)
    return attribute_list


def _choose_best_attribute(data, attributes_index, attributes_kinds, class_index, m):
    attributes_list = _take_m(attributes_kinds, m)

    // all_infos por enquanto é a entropia, mas tem que ser ganho
    aux = info_attributes(data, attributes_index, attributes_kinds, attributes_list, class_index)
    all_infos, all_groups, all_groups_index = aux

    // choice_index = all_infos.index(max(all_infos))
    choice_index = all_infos.index(min(all_infos))

    choice_name, choice_kind = attributes_list[choice_index]
    choice_groups = all_groups[choice_index]
    choice_groups_index = all_groups_index[choice_index]

    // return all_infos[choice_index] -> junto do que ja ta ali
    return choice_name, choice_kind, choice_groups, choice_groups_index


def _generate(data, attributes_index, attributes_kinds, class_index, m=None):
    if _is_class_unique(data, class_index):
        return Tree(target_class=data[:, class_index][0])

    elif not attributes_kinds:
        return Tree(target_class=_most_frequent_class(data[:, class_index]))

    else:
        // outra forma de conseguir o best atribute (sem ser por gain)
        best_attribute = _choose_best_attribute(data, attributes_index, attributes_kinds, class_index, m)
        name, kind, grouped_data, index, ganho = best_attribute

        new_attributes = {k: v for k, v in attributes_kinds.items() if k != name}

        def gen_options():
            options = {}
            for c, group in zip(index, grouped_data):
                options[c] = _generate(group, attributes_index, new_attributes, class_index, m)
            return options

        cut = data[:, attributes_index[name]].mean() if kind == "numeric" else None

        return Tree(
            // gain=ganho,
            attribute=name,
            kind=kind,
            options=gen_options(),
            cut=cut
        )


def predict(tree, instance):
    if tree.target_class or tree.target_class == 0:
        return tree.target_class

    try:
        if tree.kind == "nominal":
            sub_tree = tree.options[instance[tree.attribute]]
        else:
            sub_tree = tree.options[instance[tree.attribute] > tree.cut]
    except KeyError:
        sub_tree = next(iter(tree.options.values()))

    return predict(sub_tree, instance)

import random
from information import info_attributes
from util import group_by_attribute
from .print import tree_to_string


def _most_frequent_class(df):
    return df['class'].value_counts().idxmax()


def _take_m(attributes, m):
    attribute_list = list(attributes.items())
    if m and len(attribute_list) >= m:
        attribute_list = random.sample(attribute_list, m)
    return attribute_list


def _choose_best_attribute(attributes, df, m):
    attribute_list = _take_m(attributes, m)
    results = info_attributes(df, attribute_list)
    choice = attribute_list[results.index(min(results))]
    return choice


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
    def generate(cls, df, attributes, m=None):
        if df['class'].nunique() == 1:
            return Tree(target_class=df['class'].iloc[0])

        elif not attributes:
            return Tree(target_class=_most_frequent_class(df))

        else:
            best_attribute = _choose_best_attribute(attributes, df, m)
            name, kind = best_attribute

            groups = group_by_attribute(best_attribute, df)
            new_attributes = {k: v for k, v in attributes.items() if k != name}

            def gen_options():
                return {c: cls.generate(group, new_attributes, m) for c, group in groups}

            cut = df[name].mean() if kind == "numeric" else None

            return Tree(
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

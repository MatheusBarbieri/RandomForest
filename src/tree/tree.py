import random
from information import info_attribute
from util import group_by_attribute
from .print import tree_to_string


def _most_frequent_class(df):
    return df['class'].value_counts().idxmax()


def _choose_best_attribute(attributes, df, m):
    attribute = list(attributes.items())

    if m and len(attribute) >= m:
        attribute = random.sample(attribute, m)

    results = [info_attribute(a, df) for a in attribute]
    choice = attribute[results.index(min(results))]
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

    def predict(self, instance):
        if self.target_class:
            return (self.target_class, instance['class'])

        if self.kind == "nominal":
            sub_tree = self.options[instance[self.attribute]]
        else:
            sub_tree = self.options[instance[self.attribute] > self.cut]

        return sub_tree.predict(instance)

    def predict_df(self, instances):
        results = []
        for index, instance in instances.iterrows():
            predicted, expected = self.predict(instance.to_dict())
            results.append((predicted, expected, index))
        return results

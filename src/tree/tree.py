import random
from information import gain
from util import group_by_attribute
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
    def _choose_best_attribute(cls, attributes, df, m, seed=42):
        attr = list(attributes.items())

        if m and len(attr) >= m:
            random.seed(seed)
            attr = random.sample(attr, m)

        results = [gain(a, df) for a in attr]
        choice = attr[results.index(max(results))]
        return choice

    @classmethod
    def _most_frequent_class(cls, df):
        return df['class'].value_counts().idxmax()

    @classmethod
    def generate_node(cls, df, attributes, m=None):
        if df['class'].nunique() == 1:
            return Tree(target_class=df['class'].iloc[0])

        elif not attributes:
            return Tree(target_class=cls._most_frequent_class(df))

        else:
            best_attribute = cls._choose_best_attribute(attributes, df, m)
            name, kind = best_attribute

            groups = group_by_attribute(best_attribute, df)
            new_attributes = {k: v for k, v in attributes.items() if k != name}

            def gen_options():
                return {c: cls.generate_node(df, new_attributes, m) for c, df in groups}

            cut = df[name].mean() if kind == "numeric" else None

            return Tree(
                attribute=name,
                kind=kind,
                options=gen_options(),
                cut=cut
            )

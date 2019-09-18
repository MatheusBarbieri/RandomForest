import random
from information import info_attr
from util import group_by_attribute
from .print import tree_to_string


def _most_frequent_class(df):
    return df['class'].value_counts().idxmax()


def _choose_best_attribute(attributes, df, m, seed):
    attr = list(attributes.items())

    if m and len(attr) >= m:
        random.seed(seed)
        attr = random.sample(attr, m)

    results = [info_attr(a, df) for a in attr]
    choice = attr[results.index(min(results))]
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
    def generate(cls, df, attributes, m=None, seed=42):
        if df['class'].nunique() == 1:
            return Tree(target_class=df['class'].iloc[0])

        elif not attributes:
            return Tree(target_class=_most_frequent_class(df))

        else:
            best_attribute = _choose_best_attribute(attributes, df, m, seed)
            name, kind = best_attribute

            groups = group_by_attribute(best_attribute, df)
            new_attributes = {k: v for k, v in attributes.items() if k != name}

            def gen_options():
                return {c: cls.generate(df, new_attributes, m) for c, df in groups}

            cut = df[name].mean() if kind == "numeric" else None

            return Tree(
                attribute=name,
                kind=kind,
                options=gen_options(),
                cut=cut
            )

    @classmethod
    def predict(cls, df):
        for row in df.iterrows():


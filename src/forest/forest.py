from sampling import generate_bootstraps
from tree import Tree


class Forest:
    def __init__(self, trees):
        self.trees = trees

    @classmethod
    def generate(cls, train_set, attributes, ntree):
        bootstraps = generate_bootstraps(train_set, ntree)
        return Forest([Tree.generate(b, attributes) for b in bootstraps])

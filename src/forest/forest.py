from collections import Counter
from sampling import generate_bootstraps
from tree import Tree


class Forest:
    def __init__(self, trees):
        self.trees = trees

    @classmethod
    def generate(cls, train_set, attributes, ntree):
        bootstraps = generate_bootstraps(train_set, ntree)
        return Forest([Tree.generate(b, attributes) for b in bootstraps])

    def predict(self, instance):
        results = [tree.predict(instance) for tree in self.trees]
        data = Counter(results)
        result = max(results, key=data.get)
        return result

    def predict_df(self, instances):
        instances['predicted'] = instances.apply(lambda x: self.predict(x), axis=1)
        return instances[['class', 'predicted']]

import argparse


def get_args(arguments=None):
    parser = argparse.ArgumentParser(description='Random Forest Classificator')

    parser.add_argument(
        '-d',
        '--dataset',
        required=True,
        type=str,
        help="Path to csv dataset for training or classification.")

    parser.add_argument(
        '-a',
        '--attributes',
        required=True,
        type=str,
        help="Path to json object containing attributes wich will be used and its kind information.")

    parser.add_argument(
        '-s',
        '--seed',
        type=int,
        help="Seed to random numbers and sampling.")

    parser.add_argument(
        '-m',
        type=int,
        help="Number of sample attributes used on each division on tree [if not present, all attributes are used].")

    parser.add_argument(
        '-n',
        '--ntree',
        default=5,
        type=int,
        help="Number of trees generated on ensamble [default: %(default)s].")

    parser.add_argument(
        '-k',
        '--kfolds',
        default=5,
        type=int,
        help="Number of k-folds generated for cross-validation [default: %(default)s].")

    parser.add_argument(
        '-p',
        '--parallelize',
        dest='parallelize',
        action='store_true',
        help="Parallelize with 2x number of cpu cores processes on tree generation. WARNING: seed values wont work.")

    parser.add_argument(
        '-v',
        '--verbose',
        action='count')

    args = parser.parse_args(arguments)
    return args

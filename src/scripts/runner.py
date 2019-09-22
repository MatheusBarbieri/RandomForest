import subprocess

BASE_PATH = './data'

instances = [
    'dataset_31_credit-g',
    'dataset_44_spambase',
    'dataset_191_wine',
    'phpOkU53r'
    ]

instances_m = [
    [0, 3, 4, 5, 7, 8],
    [0, 3, 5, 10, 15],
    [0, 2, 3, 5, 6, 7],
    [0, 2, 3, 4, 5]
]

number_of_executions_with_each_params = 5

k_folds = [3, 5, 7, 10]
ntree = [5, 10, 15, 25, 50, 100, 250, 500, 1000, 2000, 3000, 5000, 10000]

for current_n_tree in ntree:
    for e in range(number_of_executions_with_each_params):
        for current_k_folds in k_folds:
            for instance, im in zip(instances, instances_m):
                current_dataset = f"{BASE_PATH}/{instance}.csv"
                current_attributes = f"{BASE_PATH}/{instance}.json"
                for current_m in im:

                    execution = [
                        'python', 'src/main.py',
                        '-d', str(current_dataset),
                        '-a', str(current_attributes),
                        '-k', str(current_k_folds),
                        '-n', str(current_n_tree),
                        '-p'
                        ]

                    if current_m != 0:
                        execution.append('-m')
                        execution.append(str(str(current_m)))

                    process = subprocess.Popen(execution)
                    process.wait()

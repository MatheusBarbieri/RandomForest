import subprocess

BASE_PATH = './data'

instances = [
    'dataset_44_spambase',
    'dataset_31_credit-g',
    'dataset_191_wine',
    'phpOkU53r'
    ]

number_of_executions_with_each_params = 50
exec_count = 1

k_folds = 5
ntree = [5, 10, 15, 25, 50, 100, 250, 500, 1000, 2000, 3000, 5000, 10000]

total = len(instances) * number_of_executions_with_each_params * len(ntree)

for current_n_tree in ntree:
    for e in range(number_of_executions_with_each_params):
        for instance in instances:
            current_dataset = f"{BASE_PATH}/{instance}.csv"
            current_attributes = f"{BASE_PATH}/{instance}.json"

            print(f'Execução [{exec_count}/{total}]')
            exec_count = exec_count + 1

            execution = [
                'python3', 'src/main.py',
                '-d', str(current_dataset),
                '-a', str(current_attributes),
                '-k', str(k_folds),
                '-n', str(current_n_tree),
                '-p'
                ]

            process = subprocess.Popen(execution)
            process.wait()

run-credit-g:
	python src/main.py -d "data/dataset_31_credit-g.csv" -a "data/dataset_31_credit-g.json"

run-spam-base:
	python src/main.py -d "data/dataset_44_spambase.csv" -a "data/dataset_44_spambase.json"

run-wine:
	python src/main.py -d "data/dataset_191_wine.csv" -a "data/dataset_191_wine.json"

run-vertebral-column:
	python src/main.py -d "data/phpOkU53r.csv" -a "data/phpOkU53r.json"

run-evaluate:
	python src/runner.py

setup:
	pip install -r requirements.txt -r

setup-dev:
	pip install -r requirements.txt -r requirements_dev.txt

lint:
	flake8

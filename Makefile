DAGS := airflow_trustly/dags
PWD := $(shell pwd)
TODAY := $(shell date -u +%Y%m%d)
# https://blog.emacsos.com/bootstrap-a-python-project.html

ifndef AIRFLOW_HOME
AIRFLOW_HOME := ~/airflow
endif

.PHONY: mainenv lint clean-pyc clean-build clean deploy test project-permissions install

mainenv: requirements_local.txt
	if [ ! -d mainenv ]; then virtualenv --python=python3 mainenv; fi; ./mainenv/bin/pip install -r requirements_local.txt

lint:
	pre-commit run --all-files

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -d -name '__pycache__' -exec rmdir {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean: clean-pyc clean-build
	rm -rf mainenv __pycache__

add-symlinks: clean
	# Adding symbolic links to DAGS directory for Airflow import tasks
	ln -sfF $(PWD)/gcp_config/gcp_config $(DAGS)
	# we don't want to check in our symlinked folders, that just gives larger diffs
	find * -type l >> .gitignore
	# also make sure we don't just keep adding duplicate in .gitignore
	sort -u .gitignore >> _tmp
	mv _tmp .gitignore

deploy: add-symlinks
	# deploy our code to prod/test, dependency to ensure local env look equal to GCP and vice versa
	./deploy.sh

test:
	coverage run -m pytest

coverage: test
	coverage report -m

install: add-symlinks
	# Pin dependencies according to https://airflow.apache.org/docs/stable/installation.html#getting-airflow
	pip install -r requirements_local.txt --use-deprecated=legacy-resolver \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.15/constraints-3.7.txt"
	rm -rf $(AIRFLOW_HOME)
	airflow initdb
	ln -sfF $(PWD)/$(DAGS) $(AIRFLOW_HOME)/dags
	python3 airflow_trustly/setup_connections.py

install-dev: install
	pip install -r requirements_dev.txt
	pre-commit install

salesforce-query-validation:
	python3 airflow_trustly/salesforce_query_validation.py

salesforce-schemas:
	python3 airflow_trustly/salesforce_query_validation.py --generate-schemas

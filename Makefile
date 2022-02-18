DAGS := dags
PWD := $(shell pwd)
# https://blog.emacsos.com/bootstrap-a-python-project.html

ifndef AIRFLOW_HOME
AIRFLOW_HOME := ~/airflow
endif

.PHONY: mainenv lint clean-pyc clean-build clean deploy test project-permissions install

lint:
	pre-commit run --all-files


test:
	coverage run -m pytest

coverage: test
	coverage report -m

# install: add-symlinks
install:
	# Pin dependencies according to https://airflow.apache.org/docs/stable/installation.html#getting-airflow
	pip install -r requirements_local.txt --use-deprecated=legacy-resolver \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.15/constraints-3.7.txt"
	rm -rf $(AIRFLOW_HOME)
	airflow initdb
	ln -sfF $(PWD)/$(DAGS) $(AIRFLOW_HOME)/dags

install-dev: install
	pip install -r requirements_dev.txt
	pre-commit install

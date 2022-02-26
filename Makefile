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

install: clean
	# Pin dependencies according to https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html#constraints-files
	pip install -r requirements_local.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-3.8.txt"
	rm -rf $(AIRFLOW_HOME)
	airflow db init
	ln -sfF $(PWD)/$(DAGS) $(AIRFLOW_HOME)/dags

install-dev: install
	pip install -r requirements_dev.txt

conf:
	sed -i=.bak 's/load_examples = True/load_examples = False/g' $(AIRFLOW_HOME)/airflow.cfg
	sed -i=.bak "s/# AUTH_ROLE_PUBLIC = 'Public'/AUTH_ROLE_PUBLIC = 'Admin'/g" $(AIRFLOW_HOME)/webserver_config.py

ex:
	sed -i=.bak 's/load_examples = False/load_examples = True/g' $(AIRFLOW_HOME)/airflow.cfg

## Setup
**NOTE:** It is highly recommended to create a virtual environment based on  Python 3.7 (through [pyenv](https://realpython.com/intro-to-pyenv/)) before doing `make install` as it will add a lot of Python packages.

Ensure the environment variable PROJECT_ID points to a GCP project and install airflow:
```
$ export PROJECT_ID=trustly-data-services-test
$ make install-dev
```

# commands
```
airflow webserver
```
in another terminal
```
airflow scheduler
```
you may need to do when removing dags:
```
airflow db reset
```
# DEVELOP and RUN DAGS
add folder to the dag folders and re run the scheduler

# import the libraries
from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator

# This makes scheduling easy
from airflow.utils.dates import days_ago

# Env Variables
ENV_VAR = {
    "RAW_DATA": "/etc/passwd",
    "EXTRACTED_DATA": "/tmp/extracted-data.txt",
    "TRANFORMED_DATA": "transformed-data.csv",
}


# defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "Mario Loera",
    "start_date": days_ago(2),
    "email": ["ramesh@somemail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

# define the DAG
dag = DAG(
    "my-first-dag_env",
    default_args=default_args,
    description="My first DAG",
    schedule_interval=timedelta(days=1),
    is_paused_upon_creation=False,
)

# define the tasks

# define the first task

extract = BashOperator(
    task_id="extract_01",
    bash_command='cut -d":" -f1,3,6 $RAW_DATA > $EXTRACTED_DATA',
    env=ENV_VAR,
    dag=dag,
)


# define the second task
transform_and_load = BashOperator(
    task_id="transform_01",
    bash_command='tr ":" "," < $EXTRACTED_DATA > $TRANFORMED_DATA',
    env=ENV_VAR,
    dag=dag,
)


# task pipeline
extract >> transform_and_load

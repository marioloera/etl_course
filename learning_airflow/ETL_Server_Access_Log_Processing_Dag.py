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
    "SRC_URL": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt",
    "RAW_DATA": "/tmp/web-server-access-log.txt",
    "EXTRACTED_DATA": "/tmp/extracted-data.txt",
    "CAPITALIZED_DATA": "/tmp/capitalized.txt",
    "ZIP_DATA": "/tmp/log.zip",
}

# defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "Mario Loera",
    "start_date": days_ago(1),
    "email": ["mario.loera@trustly.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    "airflow_test_ETL_Server_Access_Log_Processing",
    default_args=default_args,
    description="ETL_Server_Access_Log_Processing",
    schedule_interval=timedelta(days=1),
    is_paused_upon_creation=False,
)

# define the tasks

# define the task 'download'

download = BashOperator(
    task_id="download",
    bash_command="wget $SRC_URL -O $RAW_DATA",
    env=ENV_VAR,
    dag=dag,
)

# define the task 'extract'

extract = BashOperator(
    task_id="extract",
    bash_command='cut -d"#" -f1,4 $RAW_DATA > $EXTRACTED_DATA',
    env=ENV_VAR,
    dag=dag,
)

# define the task 'transform'

transform = BashOperator(
    task_id="transform",
    bash_command='tr "[a-z]" "[A-Z]" < $EXTRACTED_DATA > $CAPITALIZED_DATA',
    env=ENV_VAR,
    dag=dag,
)

# define the task 'load'

load = BashOperator(
    task_id="load",
    bash_command="zip $ZIP_DATA $CAPITALIZED_DATA",
    env=ENV_VAR,
    dag=dag,
)

# task pipeline

download >> extract >> transform >> load

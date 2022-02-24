from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


# Task 1.1 - Define DAG arguments
default_args = {
    "owner": "Mario Loera",
    "start_date": days_ago(0),
    # "email": ["marioloera@somemail.com"],
    # "email_on_failure": True,
    # "email_on_retry": True,
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
}

# Task 1.2 - Define the DAG
dag = DAG(
    "ETL_toll_data",
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description="Apache Airflow Final Assignment",
)

# Task 1.3 - Create a task to unzip data
SRC = "/tmp/project/airflow/dags/finalassignment/tolldata.tgz"
TARGET = "/tmp/project/airflow/dags/finalassignment/staging"
unzip_data = BashOperator(
    task_id="unzip_data",
    bash_command=f"tar zxvf {SRC} -C {TARGET}",
    dag=dag,
)

unzip_data

# airflow tasks test ETL_toll_data unzip_data 20220224
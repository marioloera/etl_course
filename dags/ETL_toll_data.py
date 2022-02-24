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
# airflow tasks test ETL_toll_data unzip_data 20220224

# Task 1.4 - Create a task to extract data from csv file
SRC = "/tmp/project/airflow/dags/finalassignment/staging/vehicle-data.csv"
TARGET = "/tmp/project/airflow/dags/finalassignment/staging/csv_data.csv"
extract_data_from_csv = BashOperator(
    task_id="extract_data_from_csv",
    bash_command=f'cut -d"," -f1-4 {SRC} > {TARGET}',
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_csv 20220224



# pipeline
unzip_data >> extract_data_from_csv
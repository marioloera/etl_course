from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


# Task 1.1 - Define DAG arguments
default_args = {
    "owner": "Mario Loera",
    "start_date": days_ago(0),
    "email": ["marioloera@somemail.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
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
STAGING = "/tmp/project/airflow/dags/finalassignment/staging"
CMD = f"tar zxvf {SRC} -C {STAGING}"
unzip_data = BashOperator(
    task_id="unzip_data",
    bash_command=CMD,
    dag=dag,
)

# airflow tasks test ETL_toll_data unzip_data 20220224

# Task 1.4 - Create a task to extract data from csv file
SRC = "/tmp/project/airflow/dags/finalassignment/staging/vehicle-data.csv"
CSV_DATA = "/tmp/project/airflow/dags/finalassignment/staging/csv_data.csv"
CMD = f"cut -d',' -f1-4 {SRC} > {CSV_DATA}"
extract_data_from_csv = BashOperator(
    task_id="extract_data_from_csv",
    bash_command=CMD,
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_csv 20220224

# Task 1.5 - Create a task to extract data from tsv file
SRC = "/tmp/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv"
TSV_DATA = "/tmp/project/airflow/dags/finalassignment/staging/tsv_data.csv"
CMD = f"tr $'\t' ',' < {SRC} | cut -d',' -f5-7 > {TSV_DATA}"
extract_data_from_tsv = BashOperator(
    task_id="extract_data_from_tsv",
    bash_command=CMD,
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_tsv 20220224

# Task 1.6 - Create a task to extract data from fixed width file
SRC = "/tmp/project/airflow/dags/finalassignment/staging/payment-data.txt"
FIXED_WITH_DATA = "/tmp/project/airflow/dags/finalassignment/staging/fixed_width_data.csv"
CMD = f"cut -c 59-67 {SRC} | tr ' ' ',' > {FIXED_WITH_DATA}"
extract_data_from_fixed_width = BashOperator(
    task_id="extract_data_from_fixed_width",
    bash_command=CMD,
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_fixed_width 20220224


end_task = BashOperator(
    task_id="end_task",
    bash_command="echo end",
    dag=dag,
)


# pipeline
unzip_data >> [
    extract_data_from_csv,
    extract_data_from_tsv,
    extract_data_from_fixed_width,
] >> end_task
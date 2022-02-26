from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from sqlalchemy import false

DIR = "/tmp/project/airflow/dags/finalassignment/staging/"
ENV_VAR = {
    "DIR": DIR,
    "TOLL_DATA_URL": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz",
    "TOLL_DATA": "tolldata.tgz",
    "VEHICLE_DATA": "vehicle-data.csv",
    "CSV_DATA": "csv_data.csv",
    "TOLLPLAZA_DATA": "tollplaza-data.tsv",
    "TSV_DATA": "tsv_data.csv",
    "PAYMENT_DATA": "payment-data.txt",
    "FIXED_WITH_DATA": "fixed_width_data.csv",
    "EXTRACTED_DATA": "extracted_data.csv",
    "TRANSFORMED_DATA": "transformed_data.csv"
}

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
    "ETL_toll_data_loop",
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description="Apache Airflow Final Assignment",
)

def get_task(task_id, with_dir=True):
    if with_dir:
        dir = DIR
    else:
        dir = None

    return BashOperator(
        task_id=task_id,
        bash_command=TASKS_CONFIG[task_id],
        env=ENV_VAR,
        cwd=dir,
        dag=dag,
    )

TASKS_CONFIG = {
    "mkdir": "mkdir -p $DIR",
    "download_data": "wget $TOLL_DATA_URL -O $TOLL_DATA",
    "unzip_data": "tar zxvf $TOLL_DATA -C $DIR",
    "extract_data_from_csv": "cut -d',' -f1-4 $VEHICLE_DATA > $CSV_DATA",
    "extract_data_from_fixed_width": "cut -c 59-67 $PAYMENT_DATA | tr ' ' ',' > $FIXED_WITH_DATA",
}

pipeline = None

for task_id in TASKS_CONFIG.keys():
    # the first task is mkdir, and need with_dir=false
    if pipeline is None:
        pipeline = get_task(task_id, with_dir=false)
        continue

    # pipeline.set_downstream(_task)  # doesn't work
    # pipeline >> _task  # doesn't work
    pipeline = pipeline >> get_task(task_id)  # this work, but only linear

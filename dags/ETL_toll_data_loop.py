from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

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

# Extra make dir
CMD = f"mkdir -p $DIR"
make_dir = BashOperator(
    task_id="make_dir",
    bash_command=CMD,
    env=ENV_VAR,
    dag=dag,
)

tasks = {
    "download_data": "wget $TOLL_DATA_URL -O $TOLL_DATA",
    "unzip_data": "tar zxvf $TOLL_DATA -C $DIR",
    "extract_data_from_csv": "cut -d',' -f1-4 $VEHICLE_DATA > $CSV_DATA",
    "extract_data_from_fixed_width": "cut -c 59-67 $PAYMENT_DATA | tr ' ' ',' > $FIXED_WITH_DATA",
}

pipeline = make_dir

for task_id, cmd in tasks.items():
    _task = BashOperator(
        task_id=task_id,
        bash_command=cmd,
        env=ENV_VAR,
        cwd=DIR,
        dag=dag,
    )
    # pipeline.set_downstream(_task)  # doesn't work
    # pipeline >> _task  # doesn't work
    pipeline = pipeline >> _task  # this work, but only linear

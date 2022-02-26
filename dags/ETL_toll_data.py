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
    "ETL_toll_data",
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
# airflow tasks test ETL_toll_data make_dir 20220224

# Download
# wget $TOLL_DATA_URL -O $TOLL_DATA
CMD = "wget $TOLL_DATA_URL -O $TOLL_DATA"
download_data = BashOperator(
    task_id="download_data",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)
# airflow tasks test ETL_toll_data download_data 20220224


# Task 1.3 - Create a task to unzip data
CMD = "tar zxvf $TOLL_DATA -C $DIR"
""" 
    -C $DIR is redundant if we dont want to sent to a different location
"""
unzip_data = BashOperator(
    task_id="unzip_data",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)

# airflow tasks test ETL_toll_data unzip_data 20220224

# Task 1.4 - Create a task to extract data from csv file

CMD = "cut -d',' -f1-4 $VEHICLE_DATA > $CSV_DATA"
extract_data_from_csv = BashOperator(
    task_id="extract_data_from_csv",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_csv 20220224

# Task 1.5 - Create a task to extract data from tsv file
CMD = "cut -d$'\t' -f5-7 $TOLLPLAZA_DATA | tr $'\t' ',' | tr -d $'\r' > $TSV_DATA"
extract_data_from_tsv = BashOperator(
    task_id="extract_data_from_tsv",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_tsv 20220224

# Task 1.6 - Create a task to extract data from fixed width file
CMD = "cut -c 59-67 $PAYMENT_DATA | tr ' ' ',' > $FIXED_WITH_DATA"
extract_data_from_fixed_width = BashOperator(
    task_id="extract_data_from_fixed_width",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)

# airflow tasks test ETL_toll_data extract_data_from_fixed_width 20220224

# Task 1.7 - Create a task to consolidate data extracted from previous tasks
CMD = "paste -d ',' $CSV_DATA $TSV_DATA $FIXED_WITH_DATA > $EXTRACTED_DATA"
consolidate_data = BashOperator(
    task_id="consolidate_data",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)

# airflow tasks test ETL_toll_data consolidate_data 20220224

# Task 1.8 - Transform and load the data
CMD = "tr '[:lower:]' '[:upper:]' < $EXTRACTED_DATA > $TRANSFORMED_DATA"
transform_data = BashOperator(
    task_id="transform_data",
    bash_command=CMD,
    env=ENV_VAR,
    cwd=DIR,
    dag=dag,
)

# airflow tasks test ETL_toll_data transform_data 20220224

extract = [
    extract_data_from_csv,
    extract_data_from_tsv,
    extract_data_from_fixed_width,
]

# pipeline
(
    make_dir >>
    download_data >>
    unzip_data >>
    extract >>
    consolidate_data >>
    transform_data
)

# pipeline
# unzip_data >> [
#     extract_data_from_csv,
#     extract_data_from_tsv,
#     extract_data_from_fixed_width,
# ] >> consolidate_data >> transform_data



# Task 1.9 - Define the task pipeline
# (
#     unzip_data >>
#     extract_data_from_csv >>
#     extract_data_from_tsv >>
#     extract_data_from_fixed_width >>
#     consolidate_data >>
#     transform_data
# )


# Task 1.10 - Submit the DAG submit_dag.jpg
"""
cp ETL_toll_data.py /tmp/project/airflow/dags/
"""

# Task 1.11 - Unpause the DAG unpause_dag.jpg
"""
airflow dags unpause ETL_toll_data
"""

# Task 1.12 - Monitor the DAG  dag_runs.jpg
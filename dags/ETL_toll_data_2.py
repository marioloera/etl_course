from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator

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
    "ETL_toll_data_2",
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

def get_sensor(file_id):
    return FileSensor(
        task_id=f"exist_{file_id}",
        poke_interval=5,
        timeout=0, # fails if it doesnt exist
        # mode="reschedule",
        # on_failure_callback=_failure_callback,
        filepath=f"{DIR}{ENV_VAR[file_id]}",
        #fs_conn_id=f'conn_filesensor_{partner}'
        dag=dag,
    )

TASKS_CONFIG = {
    "mkdir": "mkdir -p $DIR",
    "wget": "wget $TOLL_DATA_URL -O $TOLL_DATA",
    "unzip": "tar zxvf $TOLL_DATA -C $DIR",
    "ext_vehicle_data": "cut -d',' -f1-4 $VEHICLE_DATA > $CSV_DATA",
    "ext_payment_data": "cut -c 59-67 $PAYMENT_DATA | tr ' ' ',' > $FIXED_WITH_DATA",
    "ext_tollplaza_data": "cut -d$'\t' -f5-7 $TOLLPLAZA_DATA | tr $'\t' ',' | tr -d $'\r' > $TSV_DATA",
    "consolidate": "paste -d ',' $CSV_DATA $TSV_DATA $FIXED_WITH_DATA > $EXTRACTED_DATA",
    "transform": "tr '[:lower:]' '[:upper:]' < $EXTRACTED_DATA > $TRANSFORMED_DATA",
}

# pipeline
# (
#     get_task("mkdir", with_dir=False) >>
#     get_task("wget") >>
#     get_sensor("TOLL_DATA") >>
#     get_task("unzip") >> [
#         # (get_sensor("VEHICLE_DATA") >> get_task("ext_vehicle_data"))  # did not work
#         # chain(get_sensor("VEHICLE_DATA"), get_task("ext_vehicle_data")), # did not work
#         get_task("ext_tollplaza_data"),
#         get_task("ext_payment_data"),
#     ] >>
#     get_task("consolidate") >>
#     get_task("transform")
# )

# https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html
# Chain can also do pairwise dependencies for lists the same size
# dag ETL_toll_data_2_dag.png
chain(
    get_task("mkdir", with_dir=False),
    get_task("wget"),
    get_sensor("TOLL_DATA"),
    get_task("unzip"), [
        get_sensor("VEHICLE_DATA"),
        get_sensor("PAYMENT_DATA"),
        get_sensor("TOLLPLAZA_DATA"),
    ], [
        get_task("ext_vehicle_data"),
        get_task("ext_payment_data"),
        get_task("ext_tollplaza_data"),
    ],
    get_task("consolidate"),
    get_task("transform")
)

"""
    but if list is not the same saice ??
    a >> b1 >> b2 >> d
    a >> c1 >> d         

    this did not work
    chain(
        get_task("unzip") >> 
            (get_sensor("PAYMENT_DATA") >> get_task("ext_payment_data")),
            (get_sensor("TOLLPLAZA_DATA") >> get_task("ext_tollplaza_data")),     
        get_task("consolidate"),
    )
"""
"""
# another option here but not so clean
unzip = get_task("unzip")
consolidate = get_task("consolidate")
# pipeline
(
    get_task("mkdir", with_dir=False) >>
    get_task("wget") >>
    get_sensor("TOLL_DATA") >>
    unzip
)
unzip >> get_sensor("TOLLPLAZA_DATA") >> get_task("ext_tollplaza_data") >> consolidate
unzip >> get_sensor("VEHICLE_DATA") >> get_task("ext_vehicle_data") >> consolidate
unzip >> get_sensor("PAYMENT_DATA") >> get_task("ext_payment_data") >> consolidate

consolidate >> get_task("transform")
"""

"""
# another option here but not exactly the desire dag, with extra step
# pipeline
# dag ETL_toll_data_2_dag_extra_step.png
(
    get_task("mkdir", with_dir=False) >>
    get_task("wget") >>
    get_sensor("TOLL_DATA") >>
    get_task("unzip") >> [
        get_sensor("VEHICLE_DATA"),
        get_sensor("PAYMENT_DATA"),
        get_sensor("TOLLPLAZA_DATA"),
    ] >>
    DummyOperator(task_id="unzip_done", dag=dag) >> [
        get_task("ext_vehicle_data"),
        get_task("ext_payment_data"),
        get_task("ext_tollplaza_data"),
    ] >>
    get_task("consolidate") >>
    get_task("transform")
)
"""

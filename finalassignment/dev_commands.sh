# src="/tmp/project/airflow/dags/finalassignment/tolldata.tgz"
# target="/tmp/project/airflow/dags/finalassignment/staging/"

# src="tolldata.tgz"
# target="staging/"

# will be in the dag
# tar zxvf $src -C $target


# 1.4
SRC="/tmp/project/airflow/dags/finalassignment/staging/vehicle-data.csv"
TARGET="/tmp/project/airflow/dags/finalassignment/staging/csv_data.csv"
cut -d"," -f1-4 $SRC > $TARGET
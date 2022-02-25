# src="/tmp/project/airflow/dags/finalassignment/tolldata.tgz"
# target="/tmp/project/airflow/dags/finalassignment/staging/"

# src="tolldata.tgz"
# target="staging/"

# will be in the dag
# tar zxvf $src -C $target


# 1.4
# SRC="/tmp/project/airflow/dags/finalassignment/staging/vehicle-data.csv"
# TARGET="/tmp/project/airflow/dags/finalassignment/staging/csv_data.csv"
# cut -d"," -f1-4 $SRC > $TARGET


# 1.5
#SRC="/tmp/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv"
#TARGET="/tmp/project/airflow/dags/finalassignment/staging/tsv_data.csv"
#tr $'\t' ',' < $SRC | cut -d',' -f5-7 > $TARGET


# Task 1.6 - Create a task to extract data from fixed width file
# SRC="/tmp/project/airflow/dags/finalassignment/staging/payment-data.txt"
# TARGET="/tmp/project/airflow/dags/finalassignment/staging/fixed_width_data.csv"
# cut -c 59-67 $SRC | tr ' ' ',' > $TARGET


# Task 1.7 - Create a task to consolidate data extracted from previous tasks
CSV_DATA="/tmp/project/airflow/dags/finalassignment/staging/csv_data.csv"
TSV_DATA="/tmp/project/airflow/dags/finalassignment/staging/tsv_data.csv"
FIXED_WITH_DATA="/tmp/project/airflow/dags/finalassignment/staging/fixed_width_data.csv"
EXTRACTED_DATA="/tmp/project/airflow/dags/finalassignment/staging/extracted_data.csv"


# head $CSV_DATA > "./out/CSV_DATA.csv"
# head $TSV_DATA > "./out/TSV_DATA.csv"
# head $FIXED_WITH_DATA > "./out/FIXED_WITH_DATA.csv"
CSV_DATA="./out/CSV_DATA.csv"
TSV_DATA="./out/TSV_DATA.csv"
FIXED_WITH_DATA="./out/FIXED_WITH_DATA.csv"

paste -d ',' $CSV_DATA $TSV_DATA
paste -d ',' $CSV_DATA $TSV_DATA > ./out/extracted_data.csv

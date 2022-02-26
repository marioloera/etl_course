airflow tasks test ETL_toll_data extract_data_from_tsv 20220224
# airflow tasks test ETL_toll_data consolidate_data 20220224
# airflow tasks test ETL_toll_data extract_data_from_csv 20220224
# airflow tasks test ETL_toll_data_2 make_dir 20220224


TSV_DATA="tsv_data.csv"
EXTRACTED_DATA="extracted_data.csv"


cd /tmp/project/airflow/dags/finalassignment/staging

head -3 $TSV_DATA
#head -3 $EXTRACTED_DATA
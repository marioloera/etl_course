

TOLL_DATA="tolldata.tgz"
VEHICLE_DATA="vehicle-data.csv"
CSV_DATA="csv_data.csv"
TOLLPLAZA_DATA="tollplaza-data.tsv"
TSV_DATA="tsv_data.csv"
PAYMENT_DATA="payment-data.txt"
FIXED_WITH_DATA="fixed_width_data.csv"
EXTRACTED_DATA="extracted_data.csv"
TRANSFORMED_DATA="transformed_data.csv"

cd /tmp/project/airflow/dags/finalassignment/staging

# cut -d$'\t' -f5-7 $TOLLPLAZA_DATA | tr $'\t' ',' > $TSV_DATA
cut -d$'\t' -f5-7 $TOLLPLAZA_DATA | tr $'\t' ',' | tr -d $'\r' > $TSV_DATA

paste -d ',' $CSV_DATA $TSV_DATA $FIXED_WITH_DATA > $EXTRACTED_DATA

tr '[:lower:]' '[:upper:]' < $EXTRACTED_DATA > $TRANSFORMED_DATA
tail -3 $TSV_DATA
head -3 $EXTRACTED_DATA
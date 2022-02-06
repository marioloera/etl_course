# VARIABLES
SRC_URL="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"
RAW_DATA=temp/web-server-access-log.txt
EXTRACTED_DATA=temp/extracted-data.txt
CAPITALIZED_DATA=temp/capitalized.txt
ZIP_DATA=temp/log.zip

# Downlow file to overwrite if file exists, -q quite flag
wget -q $SRC_URL  -O $RAW_DATA

# Extract
cut -d"#" -f1,4 $RAW_DATA > $EXTRACTED_DATA

# transform: capitalize
tr "[a-z]" "[A-Z]" < $EXTRACTED_DATA > $CAPITALIZED_DATA

# Load: zip
zip $ZIP_DATA $CAPITALIZED_DATA


wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz"


mkdir -p /tmp/project/airflow/dags/finalassignment/staging


mv tolldata.tgz /tmp/project/airflow/dags/finalassignment/

# will be in the dag
# tar zxvf /tmp/project/airflow/dags/finalassignment/tolldata.tgz -C /tmp/project/airflow/dags/finalassignment/staging
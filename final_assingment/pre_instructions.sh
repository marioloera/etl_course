
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz"


mkdir -p ../home/project/airflow/dags/finalassignment/staging


mv tolldata.tgz ../home/project/airflow/dags/finalassignment

# will be in the dag
# tar zxvf tolldata.tgz -C ../home/project/airflow/dags/finalassignment/staging
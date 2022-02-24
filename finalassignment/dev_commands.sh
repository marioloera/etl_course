# src="../home/project/airflow/dags/finalassignment/tolldata.tgz"
# target="../home/project/airflow/dags/finalassignment/staging/"

src="tolldata.tgz"
target="staging/"

# will be in the dag
tar zxvf $src -C $target
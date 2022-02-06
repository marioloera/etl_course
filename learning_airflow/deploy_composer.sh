PROJECT_ID='trustly-data-services-test'
COMPOSER_LOCATION="gs://europe-west1-composer-env-t-48c46bd3-bucket/dags"
gsutil cp *_dag.py $COMPOSER_LOCATION

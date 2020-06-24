# Submit a PySpark job via the Cloud Dataproc Jobs API
# Requires having PROJECT_ID, CLUSTER_NAME and BUCKET_NAME set as 
# environment variables

export CLUSTER_NAME=data-cleaning
export PROJECT_ID=data-science-onramp
export BUCKET_NAME=citibikevd

gcloud dataproc jobs submit pyspark --cluster ${CLUSTER_NAME} \
    --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    --driver-log-levels root=FATAL \
    clean.py -- ${PROJECT_ID} ${BUCKET_NAME}
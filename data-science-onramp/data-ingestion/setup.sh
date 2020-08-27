# Submit a PySpark job via the Cloud Dataproc Jobs API
# Requires having CLUSTER_NAME and BUCKET_NAME set as 
# environment variables

gcloud dataproc jobs submit pyspark \
    --cluster ${CLUSTER_NAME} \
    --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    --driver-log-levels root=FATAL \
    setup.py -- ${BUCKET_NAME} new_york_citibike_trips

# Submit a PySpark job via the Cloud Dataproc Jobs API
gcloud dataproc jobs submit pyspark \
    --cluster ${CLUSTER_NAME} \
    --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    --driver-log-levels root=FATAL \
    setup.py -- ${BUCKET_NAME}

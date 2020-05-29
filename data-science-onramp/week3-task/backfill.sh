# Starting year and all months
base_year=2017
months=(01 02 03 04 05 06 07 08 09 10 11 12)

# Grab list of existing BigQuery tables
tables=$(bq ls fh-bigquery:reddit_posts) 

year=${base_year}
warm_up=true 

# Set the name of the output bucket
CLUSTER_NAME=${1}
BUCKET_NAME=${2}

for month in "${months[@]}"
  do
    # If the YYYY_MM table doesn't exist, we skip over it.
    exists="$(echo "${tables}" | grep " ${year}_${month} ")"
    if [ -z "${exists}" ]; then
      continue
    fi
    echo "${year}_${month}"

    # Submit a PySpark job via the Cloud Dataproc Jobs API
    gcloud dataproc jobs submit pyspark \
        --cluster ${CLUSTER_NAME} \
        --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
        --driver-log-levels root=FATAL \
        backfill.py \
        -- ${year} ${month} ${BUCKET_NAME} &
    sleep 5

    if ${warm_up}; then 
      sleep 10
      warm_up=false 
    fi
  done


Submit a Write job.

```
gcloud dataproc jobs submit pyspark spark_streaming_to_pubsublite.py \
    --region=us-west1 \
    --cluster=tz-spark \
    --jars=https://search.maven.org/remotecontent?filepath=com/google/cloud/pubsublite-spark-sql-streaming/0.3.1/pubsublite-spark-sql-streaming-0.3.1-with-dependencies.jar \
    --driver-log-levels=root=INFO \
    --properties=spark.master=yarn \
    -- 502009289245 us-west1-a tz-lite-topic-april
```

Submit a Read job.

```
gcloud dataproc jobs submit pyspark spark_streaming_from_pubsublite.py \
    --region=us-west1 \
    --cluster=tz-spark \
    --jars=https://search.maven.org/remotecontent?filepath=com/google/cloud/pubsublite-spark-sql-streaming/0.3.1/pubsublite-spark-sql-streaming-0.3.1-with-dependencies.jar \
    --driver-log-levels=root=INFO \
    --properties=spark.master=yarn \
    -- 502009289245 us-west1-a tz-lite-subscription-april

```

Read output looks like a df.
```
+--------------------+---------+------+---+----------------+--------------------+---------------+----------+
|        subscription|partition|offset|key|            data|   publish_timestamp|event_timestamp|attributes|
+--------------------+---------+------+---+----------------+--------------------+---------------+----------+
|projects/50200928...|        0|  1421| []|[68 65 6C 6C 6F]|2021-09-02 23:22:...|           null|        []|
|projects/50200928...|        0|  1422| []|[68 65 6C 6C 6F]|2021-09-02 23:22:...|           null|        []|
+--------------------+---------+------+---+----------------+--------------------+---------------+----------+
```
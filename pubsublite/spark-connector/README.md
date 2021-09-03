

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

```
+--------------------+---------+------+-------+--------------------+--------------------+-------------------+----------+
|        subscription|partition|offset|    key|                data|   publish_timestamp|    event_timestamp|attributes|
+--------------------+---------+------+-------+--------------------+--------------------+-------------------+----------+
|projects/50200928...|        0| 66005|testing|message-with-orde...|2021-09-03 18:16:...|1970-01-01 00:01:40|        []|
+--------------------+---------+------+-------+--------------------+--------------------+-------------------+----------+
```

```
+--------------------+---------+------+---+----+--------------------+--------------------+----------+
|        subscription|partition|offset|key|data|   publish_timestamp|     event_timestamp|attributes|
+--------------------+---------+------+---+----+--------------------+--------------------+----------+
|projects/50200928...|        0| 89523|  0|   .|2021-09-03 23:01:...|2021-09-03 22:56:...|        []|
|projects/50200928...|        0| 89524|  1|   .|2021-09-03 23:01:...|2021-09-03 22:56:...|        []|
|projects/50200928...|        0| 89525|  2|   .|2021-09-03 23:01:...|2021-09-03 22:56:...|        []|
```


Actual: 
MapType(StringType,ArrayType(BinaryType,true),true), 
expected: 
MapType(StringType,ArrayType(BinaryType,true),true).

\n=== Streaming Query ===\nIdentifier: [id = 18b886a8-a67a-4618-94f5-ac6a76bf3708, runId = 5a5a968f-b3ec-4ac7-9c11-4d21c53d9622]\nCurrent 

Committed Offsets: {RateStreamV2[rowsPerSecond=1, rampUpTimeSeconds=0, numPartitions=default: 89216}\nCurrent Available Offsets: {RateStreamV2[rowsPerSecond=1, rampUpTimeSeconds=0, numPartitions=default: 89886}\n\nCurrent State: ACTIVE\nThread State: RUNNABLE\n\nLogical Plan:\nProject [timestamp#0, value#1L, key#4, event_timestamp#8, data#13, cast(attributes#19 as map<string,array<binary>>) AS attributes#26]\n+- Project [timestamp#0, value#1L, key#4, event_timestamp#8, data#13, map(cast(value#1L as string), array(cast(cast(value#1L as string) as binary), cast(cast(value#1L as string) as binary))) AS attributes#19]\n   +- Project [timestamp#0, value#1L, key#4, event_timestamp#8, cast(. as binary) AS data#13]\n      +- Project [timestamp#0, value#1L, key#4, timestamp#0 AS event_timestamp#8]\n         +- Project [timestamp#0, value#1L, cast(cast((value#1L % cast(5 as bigint)) as string) as binary) AS key#4]\n            +- StreamingExecutionRelation RateStreamV2[rowsPerSecond=1, rampUpTimeSeconds=0, numPartitions=default, [timestamp#0, value#1L]\n'
2021-09-03 23:13:04 INFO  SparkContext:54 - Invoking stop() from shutdown hook
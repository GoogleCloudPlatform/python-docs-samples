```
gcloud dataproc clusters create pubsublite-spark --enable-component-gateway --bucket pubsublite-spark --region us-west1 --zone us-west1-a --master-machine-type e2-standard-2 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type e2-standard-2 --worker-boot-disk-size 500 --image-version 1.5-debian10 --project 
python-docs-samples-tests
```

```
export PUBSUBLITE_CLUSTER_ID=tz-spark                                                                                                               (pubsublite)
export PUBSUBLITE_BUCKET_ID=hub-dataproc 
```

Submit a Write job.

```
gcloud dataproc jobs submit pyspark spark_streaming_to_pubsublite_example.py \
    --region=us-west1 \
    --cluster=tz-spark \
    --jars=https://search.maven.org/remotecontent?filepath=com/google/cloud/pubsublite-spark-sql-streaming/0.3.1/pubsublite-spark-sql-streaming-0.3.1-with-dependencies.jar \
    --driver-log-levels=root=INFO \
    --properties=spark.master=yarn \
    -- 502009289245 us-west1-a tz-lite-topic-april
```

export HADOOP_CONF_DIR='/etc/hadoop/conf'
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


https://spark.apache.org/docs/latest/api/python/getting_started/quickstart.html

https://github.com/googleapis/java-pubsublite/pull/832


b"21/09/09 00:01:15 INFO org.spark_project.jetty.util.log: Logging initialized @2654ms to org.spark_project.jetty.util.log.Slf4jLog\n21/09/09 00:01:16 INFO org.spark_project.jetty.server.Server: jetty-9.4.z-SNAPSHOT; built: unknown; git: unknown; jvm 1.8.0_275-b01\n21/09/09 00:01:16 INFO org.spark_project.jetty.server.Server: Started @2741ms\n21/09/09 00:01:16 INFO org.spark_project.jetty.server.AbstractConnector: Started ServerConnector@29c3ccc8{HTTP/1.1, (http/1.1)}{0.0.0.0:35209}\n21/09/09 00:01:16 INFO org.apache.hadoop.yarn.client.RMProxy: Connecting to ResourceManager at tz-spark-m/10.138.0.8:8032\n21/09/09 00:01:16 INFO org.apache.hadoop.yarn.client.AHSProxy: Connecting to Application History server at tz-spark-m/10.138.0.8:10200\n21/09/09 00:01:16 INFO org.apache.hadoop.conf.Configuration: resource-types.xml not found\n21/09/09 00:01:16 INFO org.apache.hadoop.yarn.util.resource.ResourceUtils: Unable to find 'resource-types.xml'.\n21/09/09 00:01:16 INFO org.apache.hadoop.yarn.util.resource.ResourceUtils: Adding resource type - name = memory-mb, units = Mi, type = COUNTABLE\n21/09/09 00:01:16 INFO org.apache.hadoop.yarn.util.resource.ResourceUtils: Adding resource type - name = vcores, units = , type = COUNTABLE\n21/09/09 00:01:18 INFO org.apache.hadoop.yarn.client.api.impl.YarnClientImpl: Submitted application application_1630614308155_0074\nroot\n |-- key: binary (nullable = true)\n |-- event_timestamp: timestamp (nullable = true)\n |-- data: binary (nullable = true)\n\n21/09/09 00:01:25 INFO org.spark_project.jetty.server.AbstractConnector: Stopped Spark@29c3ccc8{HTTP/1.1, (http/1.1)}{0.0.0.0:0}\n"


python temp.py                                                                                             
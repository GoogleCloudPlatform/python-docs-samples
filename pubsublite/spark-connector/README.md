# Using Spark SQL Streaming with Pub/Sub Lite

The samples in this directory show how to read messages from and write messages to Pub/Sub Lite from an [Apache Spark] cluster created with [Cloud Dataproc] using the [Pub/Sub Lite Spark Connector].

Get the connector's uber jar from this [public Cloud Storage location]. Alternatively, visit this [Maven link] to download the connector's uber jar. The uber jar has a "with-dependencies" suffix. You will need to include it on the driver and executor classpaths when submitting a Spark job, typically in the `--jars` flag. 

## Before you begin

1. Install the [Cloud SDK].
   > *Note:* This is not required in [Cloud Shell]
   > because Cloud Shell has the Cloud SDK pre-installed.

1. Create a new Google Cloud project via the
   [*New Project* page] or via the `gcloud` command line tool.

   ```sh
   export PROJECT_ID=your-google-cloud-project-id
   gcloud projects create $PROJECT_ID
   ```
   Or use an existing Google Cloud project.
   ```sh
   export PROJECT_ID=$(gcloud config get-value project)
   ```

1. [Enable billing].

1. Setup the Cloud SDK to your GCP project.

   ```sh
   gcloud init
   ```

1. [Enable the APIs]: Pub/Sub Lite, Dataproc, Cloud Storage.

1. Create a Pub/Sub Lite [topic] and [subscription] in a supported [location].

   ```bash
   export TOPIC_ID=your-topic-id
   export SUBSCRIPTION_ID=your-subscription-id
   export PUBSUBLITE_LOCATION=your-location

   gcloud pubsub lite-topics create $TOPIC_ID \
     --location=$PUBSUBLITE_LOCATION \
     --partitions=2 \
     --per-partition-bytes=30GiB

   gcloud pubsub lite-subscriptions create $SUBSCRIPTION_ID \
      --location=$PUBSUBLITE_LOCATION \
      --topic=$TOPIC_ID
   ```

1. Create a Cloud Storage bucket.

   ```bash
   export BUCKET_ID=your-gcs-bucket-id

   gsutil mb gs://$BUCKET_ID
   ```

## Python setup

1. [Install Python and virtualenv].

1. Clone the `python-docs-samples` repository.

    ```bash
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

1. Navigate to the sample code directory.

    ```bash
    cd python-docs-samples/pubsublite/spark-connector
    ```

1. Create a virtual environment and activate it.

    ```bash
    python -m venv env
    source env/bin/activate
    ```
   > Once you are finished with the tutorial, you can deactivate
   > the virtualenv and go back to your global Python environment
   > by running `deactivate`.

1. Install the required packages.
    ```bash
    python -m pip install -U -r requirements.txt
    ```

## Creating a Spark cluster on Dataproc

1. Go to [Cloud Console for Dataproc].

1. Go to Clusters, then [Create Cluster].
   > **Note:** Choose [Dataproc Image Version 1.5]
   > under ___Versioning___ for Spark 2.4.8.
   > Choose [Dataproc Image Version 2.0] for Spark 3.
   > The latest connector works with Spark 3.
   > See [compatibility].
   > Additionally, in ___Manage security (optional)___, you
   > must enable the cloud-platform scope for your cluster by
   > checking "Allow API access to all Google Cloud services in
   > the same project" under ___Project access___.

   Here is an equivalent example using a `gcloud` command, with an additional optional argument to enable component gateway:

    ```sh
    export CLUSTER_ID=your-cluster-id
    export DATAPROC_REGION=your-dataproc-region

    gcloud dataproc clusters create $CLUSTER_ID \
      --region $DATAPROC_REGION \
      --image-version 2.0-debian10 \
      --scopes 'https://www.googleapis.com/auth/cloud-platform' \
      --enable-component-gateway
    ```

## Writing to Pub/Sub Lite

[spark_streaming_to_pubsublite_example.py](spark_streaming_to_pubsublite_example.py) creates a streaming source of consecutive numbers with timestamps for 60 seconds and writes them to a Pub/Sub topic.

To submit a write job:

```sh
export PROJECT_NUMBER=$(gcloud projects list --filter="projectId:$PROJECT_ID" --format="value(PROJECT_NUMBER)")

gcloud dataproc jobs submit pyspark spark_streaming_to_pubsublite_example.py \
    --region=$DATAPROC_REGION \
    --cluster=$CLUSTER_ID \
    --jars=gs://spark-lib/pubsublite/pubsublite-spark-sql-streaming-LATEST-with-dependencies.jar \
    --driver-log-levels=root=INFO \
    --properties=spark.master=yarn \
    -- --project_number=$PROJECT_NUMBER --location=$PUBSUBLITE_LOCATION --topic_id=$TOPIC_ID
```

Visit the job URL in the command output or the jobs panel in [Cloud Console for Dataproc] to monitor the job progress.

You should see INFO logging like the following in the output:

```none
INFO com.google.cloud.pubsublite.spark.PslStreamWriter: Committed 1 messages for epochId ..
```

## Reading from Pub/Sub Lite

[spark_streaming_from_pubsublite_example.py](spark_streaming_from_pubsublite_example.py) reads messages formatted as dataframe rows from a Pub/Sub subscription and prints them out to the console.

To submit a read job:

```sh
gcloud dataproc jobs submit pyspark spark_streaming_from_pubsublite_example.py \
    --region=$DATAPROC_REGION \
    --cluster=$CLUSTER_ID \
    --jars=gs://spark-lib/pubsublite/pubsublite-spark-sql-streaming-LATEST-with-dependencies.jar \
    --driver-log-levels=root=INFO \
    --properties=spark.master=yarn \
    -- --project_number=$PROJECT_NUMBER --location=$PUBSUBLITE_LOCATION --subscription_id=$SUBSCRIPTION_ID
```

Here is an example output: <!--TODO: update attributes field output with the next release of the connector-->

```none
+--------------------+---------+------+---+----+--------------------+--------------------+----------+
|        subscription|partition|offset|key|data|   publish_timestamp|     event_timestamp|attributes|
+--------------------+---------+------+---+----+--------------------+--------------------+----------+
|projects/50200928...|        0| 89523|  0|   .|2021-09-03 23:01:...|2021-09-03 22:56:...|        []|
|projects/50200928...|        0| 89524|  1|   .|2021-09-03 23:01:...|2021-09-03 22:56:...|        []|
|projects/50200928...|        0| 89525|  2|   .|2021-09-03 23:01:...|2021-09-03 22:56:...|        []|
```

[Apache Spark]: https://spark.apache.org/
[Pub/Sub Lite Spark Connector]: https://github.com/googleapis/java-pubsublite-spark
[Cloud Dataproc]: https://cloud.google.com/dataproc/docs/
[public Cloud Storage location]: gs://spark-lib/pubsublite/pubsublite-spark-sql-streaming-LATEST-with-dependencies.jar
[Maven link]: https://search.maven.org/search?q=g:com.google.cloud%20a:pubsublite-spark-sql-streaming

[Cloud SDK]: https://cloud.google.com/sdk/docs/
[Cloud Shell]: https://console.cloud.google.com/cloudshell/editor/
[*New Project* page]: https://console.cloud.google.com/projectcreate
[Enable billing]: https://cloud.google.com/billing/docs/how-to/modify-project/
[Enable the APIs]: https://console.cloud.google.com/flows/enableapi?apiid=pubsublite.googleapis.com,dataproc,storage_component
[topic]: https://cloud.google.com/pubsub/lite/docs/topics
[subscription]: https://cloud.google.com/pubsub/lite/docs/subscriptions
[location]: https://cloud.google.com/pubsub/lite/docs/locations

[Install Python and virtualenv]: https://cloud.google.com/python/setup/
[Cloud Console for Dataproc]: https://console.cloud.google.com/dataproc/

[Create Cluster]: https://pantheon.corp.google.com/dataproc/clustersAdd
[Dataproc Image Version 1.5]: https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-release-1.5
[Dataproc Image Version 2.0]: https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-release-2.0
[compatability]: gs://spark-lib/pubsublite/pubsublite-spark-sql-streaming-LATEST-with-dependencies.jar
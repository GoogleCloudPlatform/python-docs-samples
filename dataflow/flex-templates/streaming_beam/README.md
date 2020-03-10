# Dataflow flex templates - Streaming Beam

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor)

Samples showing how to create and run an
[Apache Beam](https://beam.apache.org/) template with a custom Docker image on
[Google Cloud Dataflow](https://cloud.google.com/dataflow/docs/).

## Before you begin

Follow the
[Getting started with Google Cloud Dataflow](../README.md)
page, and make sure you have a Google Cloud project with billing enabled
and a *service account JSON key* set up in your `GOOGLE_APPLICATION_CREDENTIALS`
environment variable.
Additionally, for this sample you need the following:

1. Create a
   [Cloud Storage bucket](https://cloud.google.com/storage/docs/creating-buckets).

    ```sh
    export BUCKET="your-gcs-bucket"
    gsutil mb gs://$BUCKET
    ```

1. Create a
   [Pub/Sub topic](https://cloud.google.com/pubsub/docs/admin#creating_a_topic)
   and a
   [subscription](https://cloud.google.com/pubsub/docs/admin#creating_subscriptions)
   to that topic.

    ```sh
    # For simplicity we use the same topic name as the subscription name.
    export TOPIC="messages"
    export SUBSCRIPTION="$TOPIC"

    gcloud pubsub topics create $TOPIC
    gcloud pubsub subscriptions create --topic $TOPIC $SUBSCRIPTION
    ```

1. Create a
   [Cloud Scheduler job](https://cloud.google.com/scheduler/docs/quickstart)
   to publish
   [1 message per minute](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules).

    ```sh
    # If an App Engine app does not exist for the project, this step will create one.
    gcloud scheduler jobs create pubsub thumbs-up-publisher \
      --schedule="* * * * *" \
      --topic="$TOPIC" \
      --message-body='{"url": "https://beam.apache.org/", "review": "positive"}'

    # Start the job.
    gcloud scheduler jobs run thumbs-up-publisher

    # Now, let's create a similar publisher for thumbs down, but publish
    # 1 message every 2 minutes.
    gcloud scheduler jobs create pubsub thumbs-down-publisher \
      --schedule="*/2 * * * *" \
      --topic="$TOPIC" \
      --message-body='{"url": "https://beam.apache.org/", "review": "negative"}'

    gcloud scheduler jobs run thumbs-down-publisher
    ```

1. Create a [BigQuery dataset](https://cloud.google.com/bigquery/docs/datasets).

    ```sh
    export PROJECT="$(gcloud config get-value project)"
    export DATASET="beam_samples"
    export TABLE="streaming_beam"

    bq mk --dataset "$PROJECT:$DATASET"
    ```

1. Clone the `python-docs-samples` repository and navigate to the code sample.

    ```sh
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    cd python-docs-samples/dataflow/flex-templates/streaming_beam
    ```

1. Create a virtual environment and activate it.

   ```sh
   virtualenv env
   source env/bin/activate
   ```

   > Once you are done, you can deactivate the virtualenv and go back to your global Python environment by running `deactivate`.

1. Install the sample requirements.

   ```sh
   pip install -U -r requirements.txt
   ```

## Pub/Sub to BigQuery with Beam sample

This sample shows how to deploy an Apache Beam streaming pipeline that reads
[JSON encoded](https://www.w3schools.com/whatis/whatis_json.asp) messages from
[Pub/Sub](https://cloud.google.com/pubsub),
to transform the message data, and writes the results to a
[BigQuery](https://cloud.google.com/bigquery) table.

* [Dockerfile](Dockerfile)
* [streaming_beam.py](streaming_beam.py)
* [metadata.json](metadata.json)

### Build the container image

We will build the
[Docker](https://docs.docker.com/engine/docker-overview/)
image for the Apache Beam pipeline.
We are using
[Cloud Build](https://cloud.google.com/cloud-build)
so we don't need a local installation of Docker.

> *Note:* You can speed up subsequent builds with
> [Kaniko cache](https://cloud.google.com/cloud-build/docs/kaniko-cache)
> in Cloud Build.
>
> ```sh
> # [optional] Enable to use Kaniko cache by default.
> gcloud config set builds/use_kaniko True
> ```

Cloud Build allows you to
[build a Docker image using a `Dockerfile`](https://cloud.google.com/cloud-build/docs/quickstart-docker#build_using_dockerfile).
and saves it into
[Container Registry](https://cloud.google.com/container-registry/),
where the image is accessible to other Google Cloud products.

Images starting with `gcr.io/<PROJECT>/` are saved into your project's
Container Registry.

```sh
export TEMPLATE_IMAGE="gcr.io/$PROJECT/samples/dataflow/streaming-beam:latest"

# Build the image into Container Registry, this is roughly equivalent to:
#   gcloud auth configure-docker
#   docker image build -t $TEMPLATE_IMAGE .
#   docker push $TEMPLATE_IMAGE
gcloud builds submit --tag $TEMPLATE_IMAGE .
```

### Creating the Dataflow Flex Template

To run a template, we need to create a *template spec* file containing all the
information necessary to run the job, such as the SDK information and metadata.

The [`metadata.json`](metadata.json) file contains more information for the
template such as the name, a description and the list of input parameters.

The template file must be created in a Cloud Storage location,
and is used to run a new Dataflow job.

We can build the Dataflow Flex template via the
[`gcloud dataflow flex-templates build`](https://cloud.google.com/sdk/gcloud/reference/beta/dataflow/flex-templates/build)
command.

```sh
export TEMPLATE_PATH="gs://$BUCKET/samples/dataflow/templates/streaming-beam.json"

# Option A: Build the template via `gcloud`.
gcloud dataflow flex-templates build $TEMPLATE_PATH \
  --image "$TEMPLATE_IMAGE" \
  --sdk-language "PYTHON" \
  --metadata-file "metadata.json"

# Option B: Copy the template.json file to a Cloud Storage location.
# NOTE: we need to set the image path to the one in the project it was built.
sed "s|<IMAGE>|$TEMPLATE_IMAGE|g" template.json | gsutil cp - $TEMPLATE_PATH
```

The template is now available through the template file in the
Cloud Storage location we saved it.

### Running a Dataflow Flex Template pipeline

Users can now run the Apache Beam pipeline in Dataflow by simply referring
to the template file and passing the template parameters required by
the pipeline.

Once a template is created, it's easy to run via the
[`gcloud dataflow flex-templates run`](https://cloud.google.com/sdk/gcloud/reference/beta/dataflow/flex-templates/run)
command.
There is no need to modify any code for users running a deployed template.

```sh
# Option A: Run the template via `gcloud`.
# Parameters before the `--` are passed to the `gcloud` command.
# Parameters after the `--` are passed to the pipeline.
# We can optionally still pass other standard PipelineOptions,
# such as `--workerMachineType`, flags alongside other template parameters.
gcloud dataflow flex-templates run "streaming-beam-`date +%Y%m%d-%H%M%S`"
  --template-file-gcs-location $TEMPLATE_PATH \
  -- \
  --input_topic "$TOPIC" \
  --output_table "$PROJECT:$DATASET.$TABLE" \
  --workerMachineType "e2-micro"  # optional PipelineOptions flag

# Option B: Run via a POST request using curl.
curl -X POST \
  "https://dataflow-staging.sandbox.googleapis.com/v1b3/projects/$PROJECT/locations/us-central1/flexTemplates:launch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d '{
    "launch_parameter": {
      "jobName": "streaming-beam-'$(date +%Y%m%d-%H%M%S)'",
      "parameters": {
        "input_topic": "'$TOPIC'",
        "output_table": "'$PROJECT:$DATASET.$TABLE'"
      },
      "container_spec_gcs_path": "'$TEMPLATE_PATH'"
    }
  }'
```

> To learn more about the supported `PipelineOptions`, see the
> [Setting other Cloud Dataflow pipeline options](https://cloud.google.com/dataflow/docs/guides/specifying-exec-params#setting-other-cloud-dataflow-pipeline-options) page.

Now that your Dataflow pipeline is running, you should be able to see new rows
being appended into the BigQuery table every minute or so,
depending on the window size in your Dataflow job.

Run the following query to check the results in BigQuery.

```sh
bq query --use_legacy_sql=false 'SELECT * FROM `'"$PROJECT.$DATASET.$TABLE"'`'
```

You can manually publish more messages from the
[Cloud Scheduler page](https://console.cloud.google.com/cloudscheduler)
to see how that affects the page review scores.

You can also publish messages directly to a topic through the
[Pub/Sub topics page](https://console.cloud.google.com/cloudpubsub/topic/list)
by selecting the topic you want to publish to,
and then clicking the "Publish message" button at the top.
This way you can test your pipeline with different URLs,
just make sure you pass valid JSON data since this sample does not do any
error handling for code simplicity.

Try sending the following message and check back the BigQuery table about
a minute later.

```json
{"url": "https://cloud.google.com/bigquery/", "review": "positive"}
```

### Clean up

To avoid incurring charges to your Google Cloud account for the resources used
in this guide, follow these steps.

Clean up the Dataflow Flex template resources.

```sh
# Stop the Dataflow pipeline.
gcloud dataflow jobs list \
    --filter 'NAME:streaming-beam AND STATE=Running' \
    --format 'value(JOB_ID)' \
  | xargs gcloud dataflow jobs cancel

# Delete the template spec file from Cloud Storage.
gsutil rm $TEMPLATE_PATH

# Delete the Flex Template container image from Container Registry.
gcloud container images delete $TEMPLATE_IMAGE --force-delete-tags
```

Clean up project resources.

```sh
# Delete the Cloud Scheduler jobs.
gcloud scheduler jobs delete thumbs-down-publisher
gcloud scheduler jobs delete thumbs-up-publisher

# Delete the Pub/Sub subscription and topic.
gcloud pubsub subscriptions delete $SUBSCRIPTION
gcloud pubsub topics delete $TOPIC

# Delete the BigQuery table.
bq rm -f -t $PROJECT:$DATASET.$TABLE

# Delete the BigQuery dataset, this alone does not incur any charges.
# WARNING: The following command also deletes all tables in the dataset.
#          The tables and data cannot be recovered.
bq rm -r -f -d $PROJECT:$DATASET

# Delete the Cloud Storage bucket, this alone does not incur any charges.
# WARNING: The following command also deletes all objects in the bucket.
#          These objects cannot be recovered.
gsutil rm -r gs://$BUCKET
```

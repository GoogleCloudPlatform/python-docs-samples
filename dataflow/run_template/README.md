# Run template

[`main.py`](main.py) - Script to run an [Apache Beam] template on [Google Cloud Dataflow].

The following examples show how to run the [`Word_Count` template], but you can run any other template.

For the `Word_Count` template, we require to pass an `output` Cloud Storage path prefix, and optionally we can pass an `inputFile` Cloud Storage file pattern for the inputs.
If `inputFile` is not passed, it will take `gs://apache-beam-samples/shakespeare/kinglear.txt` as default.

## Before you begin

1. Install the [Cloud SDK].

1. [Create a new project].

1. [Enable billing].

1. [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=dataflow,compute_component,logging,storage_component,storage_api,bigquery,pubsub,datastore.googleapis.com,cloudfunctions.googleapis.com,cloudresourcemanager.googleapis.com): Dataflow, Compute Engine, Stackdriver Logging, Cloud Storage, Cloud Storage JSON, BigQuery, Pub/Sub, Datastore, Cloud Functions, and Cloud Resource Manager.

1. Setup the Cloud SDK to your GCP project.

   ```bash
   gcloud init
   ```

1. Create a Cloud Storage bucket.

   ```bash
   gsutil mb gs://your-gcs-bucket
   ```

## Setup

The following instructions will help you prepare your development environment.

1. [Install Python and virtualenv].

1. Clone the `python-docs-samples` repository.

    ```bash
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

1. Navigate to the sample code directory.

   ```bash
   cd python-docs-samples/dataflow/run_template
   ```

1. Create a virtual environment and activate it.

   ```bash
   virtualenv env
   source env/bin/activate
   ```

   > Once you are done, you can deactivate the virtualenv and go back to your global Python environment by running `deactivate`.

1. Install the sample requirements.

   ```bash
   pip install -U -r requirements.txt
   ```

## Running locally

To run a Dataflow template from the command line.

> NOTE: To run locally, you'll need to [create a service account key] as a JSON file.
> Then export an environment variable called `GOOGLE_APPLICATION_CREDENTIALS` pointing it to your service account file.

```bash
python main.py \
  --project <your-gcp-project> \
  --job wordcount-$(date +'%Y%m%d-%H%M%S') \
  --template gs://dataflow-templates/latest/Word_Count \
  --inputFile gs://apache-beam-samples/shakespeare/kinglear.txt \
  --output gs://<your-gcs-bucket>/wordcount/outputs
```

## Running in Python

To run a Dataflow template from Python.

> NOTE: To run locally, you'll need to [create a service account key] as a JSON file.
> Then export an environment variable called `GOOGLE_APPLICATION_CREDENTIALS` pointing it to your service account file.

```py
import main as run_template

run_template.run(
    project='your-gcp-project',
    job='unique-job-name',
    template='gs://dataflow-templates/latest/Word_Count',
    parameters={
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://<your-gcs-bucket>/wordcount/outputs',
    }
)
```

## Running in Cloud Functions

To deploy this into a Cloud Function and run a Dataflow template via an HTTP request as a REST API.

```bash
PROJECT=$(gcloud config get-value project) \
REGION=$(gcloud config get-value functions/region)

# Deploy the Cloud Function.
gcloud functions deploy run_template \
  --runtime python37 \
  --trigger-http \
  --region $REGION

# Call the Cloud Function via an HTTP request.
curl -X POST "https://$REGION-$PROJECT.cloudfunctions.net/run_template" \
  -d project=$PROJECT \
  -d job=wordcount-$(date +'%Y%m%d-%H%M%S') \
  -d template=gs://dataflow-templates/latest/Word_Count \
  -d inputFile=gs://apache-beam-samples/shakespeare/kinglear.txt \
  -d output=gs://<your-gcs-bucket>/wordcount/outputs
```

[Apache Beam]: https://beam.apache.org/
[Google Cloud Dataflow]: https://cloud.google.com/dataflow/docs/
[`Word_Count` template]: https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/master/src/main/java/com/google/cloud/teleport/templates/WordCount.java

[Cloud SDK]: https://cloud.google.com/sdk/docs/
[Create a new project]: https://console.cloud.google.com/projectcreate
[Enable billing]: https://cloud.google.com/billing/docs/how-to/modify-project
[Create a service account key]: https://console.cloud.google.com/apis/credentials/serviceaccountkey
[Creating and managing service accounts]: https://cloud.google.com/iam/docs/creating-managing-service-accounts
[GCP Console IAM page]: https://console.cloud.google.com/iam-admin/iam
[Granting roles to service accounts]: https://cloud.google.com/iam/docs/granting-roles-to-service-accounts

[Install Python and virtualenv]: https://cloud.google.com/python/setup

# Run template

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/run_template/README.md)

This sample demonstrate how to run an
[Apache Beam](https://beam.apache.org/)
template on [Google Cloud Dataflow](https://cloud.google.com/dataflow/docs/).
For more information, see the
[Running templates](https://cloud.google.com/dataflow/docs/guides/templates/running-templates)
docs page.

The following examples show how to run the
[`Word_Count` template](https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/master/src/main/java/com/google/cloud/teleport/templates/WordCount.java),
but you can run any other template.

For the `Word_Count` template, we require to pass an `output` Cloud Storage path prefix,
and optionally we can pass an `inputFile` Cloud Storage file pattern for the inputs.
If `inputFile` is not passed, it will take `gs://apache-beam-samples/shakespeare/kinglear.txt` as default.

## Before you begin

Follow the
[Getting started with Google Cloud Dataflow](../README.md)
page, and make sure you have a Google Cloud project with billing enabled
and a *service account JSON key* set up in your `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
Additionally, for this sample you need the following:

1. Create a Cloud Storage bucket.

   ```sh
   export BUCKET=your-gcs-bucket
   gsutil mb gs://$BUCKET
   ```

1. Clone the `python-docs-samples` repository.

   ```sh
   git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
   ```

1. Navigate to the sample code directory.

   ```sh
   cd python-docs-samples/dataflow/run_template
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

## Running locally

* [`main.py`](main.py)
* [REST API dataflow/projects.templates.launch](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.templates/launch)

To run a Dataflow template from the command line.

```sh
python main.py \
  --project <your-gcp-project> \
  --job wordcount-$(date +'%Y%m%d-%H%M%S') \
  --template gs://dataflow-templates/latest/Word_Count \
  --inputFile gs://apache-beam-samples/shakespeare/kinglear.txt \
  --output gs://<your-gcs-bucket>/wordcount/outputs
```

## Running in Python

* [`main.py`](main.py)
* [REST API dataflow/projects.templates.launch](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.templates/launch)

To run a Dataflow template from Python.

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

* [`main.py`](main.py)
* [REST API dataflow/projects.templates.launch](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.templates/launch)

To deploy this into a Cloud Function and run a Dataflow template via an HTTP request as a REST API.

```sh
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

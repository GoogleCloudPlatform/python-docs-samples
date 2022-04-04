# Minimal custom container

This sample runs a Dataflow pipeline where the workers use a custom minimal Python slim container image.

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md).

You will also need:
* A Cloud Storage bucket, click [here to create one](https://console.cloud.google.com/storage/create-bucket) if needed.

```sh
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-cloud-storage-bucket"
```

> ℹ️ Make sure your `BUCKET` name does _not_ include the `gs://` prefix.

## Building the Docker image

We use
[Cloud Build](https://cloud.google.com/build)
to build the container image for the workers and save it in
[Container Registry](https://cloud.google.com/container-registry/).

```sh
export IMAGE=gcr.io/$PROJECT/samples/dataflow-slim:latest

gcloud builds submit . --tag=$IMAGE
```

## Running the Dataflow job

We use Cloud Build to run the [Dataflow](https://cloud.google.com/dataflow) job.

The [`run.yaml`](run.yaml) file contains the command we use to launch the Dataflow job.

> ℹ️ We launch the job using the worker image to make sure the job launches
> with the same Python version as the workers and all the dependencies installed.

```sh
# Choose the location where you want to run your Dataflow job.
# For a list of all supported locations, see:
#   https://cloud.google.com/dataflow/docs/resources/locations
export REGION="us-central1"

export JOB_NAME="dataflow-slim-$(date +"%F-%H%M%S")"
export TEMP_LOCATION="gs://$BUCKET/samples/dataflow-slim"

gcloud builds submit \
    --config run.yaml \
    --substitutions "_JOB_NAME=$JOB_NAME,_REGION=$REGION,_TEMP_LOCATION=$TEMP_LOCATION" \
    --no-source
```

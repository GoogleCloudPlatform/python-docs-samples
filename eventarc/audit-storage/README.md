# Cloud Eventarc - Cloud Storage via Audit Logs tutorial

This sample shows how to create a service that processes GCS using [the CloudEvents SDK](https://github.com/cloudevents/sdk-python).

## Setup

Configure environment variables:

```sh
MY_RUN_SERVICE=gcs-service
MY_RUN_CONTAINER=gcs-container
MY_GCS_BUCKET=gcs-bucket # Must be globally unique.
```

## Quickstart

Deploy your Cloud Run service:

```sh
gcloud builds submit \
  --tag gcr.io/$(gcloud config get-value project)/$MY_RUN_CONTAINER
gcloud run deploy $MY_RUN_SERVICE \
  --image gcr.io/$(gcloud config get-value project)/$MY_RUN_CONTAINER \
  --platform managed
```

Create a _single region_ Cloud Storage bucket:

```sh
gsutil mb -p $(gcloud config get-value project) \
  -l us-central1 \
  gs://"$MY_GCS_BUCKET"
```

Create Cloud Storage trigger:

```sh
gcloud beta eventarc triggers create my-gcs-trigger \
  --destination-run-service $MY_RUN_SERVICE  \
  --matching-criteria type=google.cloud.audit.log.v1.written \
  --matching-criteria methodName=storage.buckets.update \
  --matching-criteria serviceName=storage.googleapis.com \
  --matching-criteria resourceName=projects/_/buckets/"$MY_GCS_BUCKET"
```

## Test

Test your Cloud Run service by creating a GCS event:

```sh
gsutil defstorageclass set STANDARD gs://$MY_GCS_BUCKET
```

Observe the Cloud Run service printing upon receiving an event in Cloud Logging:

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
  resource.labels.service_name=$MY_RUN_SERVICE" \
  --project $(gcloud config get-value project) \
  --limit 30 \
  --format 'value(textPayload)'
```

One of the logs you'll see shows the Run service confirming the event was received:

```
GCS CloudEvent type: storage.googleapis.com/projects/_/buckets/gcs-bucket
```
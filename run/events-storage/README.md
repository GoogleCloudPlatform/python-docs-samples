# Events for Cloud Run – GCS tutorial

This sample shows how to create a service that processes GCS using [the CloudEvents SDK](https://github.com/cloudevents/sdk-python).

## Setup

Login to gcloud:

```sh
gcloud auth login
```

Configure project id:

```sh
gcloud config set project [PROJECT-ID]
```

Configure environment variables:

```sh
MY_RUN_SERVICE=gcs-service
MY_RUN_CONTAINER=gcs-container
MY_GCS_TRIGGER=gcs-trigger
MY_GCS_BUCKET=gcs-bucket
```

## Quickstart

Deploy your Cloud Run service:

```sh
gcloud builds submit \
 --tag gcr.io/$(gcloud config get-value project)/$MY_RUN_CONTAINER
gcloud run deploy $MY_RUN_SERVICE \
 --image gcr.io/$(gcloud config get-value project)/$MY_RUN_CONTAINER \
 --allow-unauthenticated
```

Create a bucket:

```sh
gsutil mb -p $(gcloud config get-value project) -l \
us-central1 gs://"$MY_GCS_BUCKET"
```

Create Cloud Storage trigger:

```sh
gcloud alpha events triggers create $MY_GCS_TRIGGER \
 --target-service "$MY_RUN_SERVICE" \
 --type com.google.cloud.auditlog.event \
 --parameters methodName=storage.buckets.update \
 --parameters serviceName=storage.googleapis.com \
 --parameters resourceName=projects/_/buckets/"$MY_GCS_BUCKET"
```

## Test

Test your Cloud Run service by publishing a message to the topic:

```sh
gsutil defstorageclass set STANDARD gs://$MY_GCS_BUCKET
```

Observe the Cloud Run service printing upon receiving an event in
Cloud Logging:

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=$MY_RUN_SERVICE" --project \
$(gcloud config get-value project) --limit 30 --format 'value(textPayload)'
```

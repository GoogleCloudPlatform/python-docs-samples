# Events for Cloud Run – Pub/Sub tutorial

This sample shows how to create a service that processes GCS events

## Setup

```sh
gcloud auth login
```

```sh
gcloud config set project [PROJECT-ID]
```

```sh
MY_RUN_SERVICE=gcs-service
MY_RUN_CONTAINER=gcs-container

MY_TOPIC=gcs-topic

MY_PUBSUB_TRIGGER=pubsub-trigger
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

Create a bucket 

```sh
gsutil mb -p $(gcloud config get-value project) -l \
us-central1 gs://"$MY_GCS_BUCKET"
```

Create a Cloud Pub/Sub topic:

```sh
gcloud pubsub topics create $MY_TOPIC
```

Create a Cloud Pub/Sub trigger:

```sh
gcloud alpha events triggers create $MY_PUBSUB_TRIGGER \
--target-service $MY_RUN_SERVICE \
--type com.google.cloud.pubsub.topic.publish \
--parameters topic=$MY_TOPIC
```

Create Cloud Storage trigger

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
gsutil defstorageclass set NEARLINE gs://$MY_GCS_BUCKET
```

You may observe the Run service receiving an event in Cloud Logging.
```sh
gcloud logging read "projects/$(gcloud config get-value \
project)/logs/cloudaudit.googleapis.com%2Factivity" --format=json
```
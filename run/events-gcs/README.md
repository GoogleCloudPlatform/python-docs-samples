# Events for cloud run Google Cloud Storage tutorial

This sample shows how to create a service that processes authenticated Cloud 
Storage events. 

## Setup

First ensure you are authorized to your gcloud account via 

```sh
gcloud auth login
```

Then make sure your project is configured via

```sh
gcloud config set project [PROJECT-ID]
```

Configure with environment variables

```sh
MY_RUN_CONTAINER=events-container
MY_RUN_SERVICE=hello-events
MY_GCS_BUCKET=single-region-bucket
```

## Quickstart

Create and upload your service

```sh
gcloud builds submit \
 --tag gcr.io/$(gcloud config get-value project)/"$MY_RUN_CONTAINER"
gcloud run deploy "$MY_RUN_SERVICE" \
 --image gcr.io/$(gcloud config get-value project)/"$MY_RUN_CONTAINER"
```

Create a bucket

```sh
gsutil mb -p $(gcloud config get-value project) -l \
us-central1 gs://"$MY_GCS_BUCKET"
```

Create a trigger

```sh
gcloud alpha events triggers create my-gcs-trigger \
 --target-service "$MY_RUN_SERVICE" \
 --type com.google.cloud.auditlog.event \
 --parameters methodName=storage.buckets.update \
 --parameters serviceName=storage.googleapis.com \
 --parameters resourceName=projects/_/buckets/"$MY_GCS_BUCKET" 
```

Send event

```sh
gsutil defstorageclass set NEARLINE gs://$MY_GCS_BUCKET
gsutil defstorageclass set STANDARD gs://$MY_GCS_BUCKET
```

Read logs

```sh
gcloud logging read "projects/$(gcloud config get-value \
project)/logs/cloudaudit.googleapis.com%2Factivity" --format=json
```

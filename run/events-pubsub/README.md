# Events for Cloud Run – Pub/Sub tutorial

This sample shows how to create a service that processes Pub/Sub events using 
[the CloudEvents SDK](https://github.com/cloudevents/sdk-python).

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
MY_RUN_SERVICE=pubsub-service
MY_RUN_CONTAINER=pubsub-container
MY_TOPIC=pubsub-topic
MY_PUBSUB_TRIGGER=pubsub-trigger
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

## Test

Test your Cloud Run service by publishing a message to the topic: 

```sh
gcloud pubsub topics publish $MY_TOPIC --message="John Doe"
```

You may observe the Cloud Run service printing upon receiving an event in 
Cloud Logging.

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=$MY_RUN_SERVICE" --project \
$(gcloud config get-value project) --limit 30 --format 'value(textPayload)'
```

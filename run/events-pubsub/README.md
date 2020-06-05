# Events for Cloud Run – Pub/Sub tutorial

This sample shows how to create a service that processes Authenticated Pub/Sub messages.

## Setup

First ensure you are authorized to your gcloud account via 

```sh
gcloud auth login
```

Then make sure your project is configured via

```sh
gcloud config set project [PROJECT-ID]
```

## Quickstart

Deploy your Cloud Run service:

```sh
gcloud builds submit \
 --tag gcr.io/$(gcloud config get-value project)/cloudrun-events-pubsub
gcloud run deploy cloudrun-events-pubsub \
 --image gcr.io/$(gcloud config get-value project)/cloudrun-events-pubsub
```

When asked if you want to allow unauthenticateddd invocations, say no 

Retrieve container URL from the gcloud run deploy command executed above and store it as seen below

```sh
MY_RUN_SERVICE=<container_running_instance_url>
```

Create a Cloud Pub/Sub topic:

```sh
gcloud pubsub topics create my-topic
```

Create a Cloud Pub/Sub trigger:

```sh
gcloud alpha events triggers create pubsub-trigger \
--target-service cloudrun-events-pubsub \
--type com.google.cloud.pubsub.topic.publish \
--parameters topic=my-topic
```

Enable authenticated calls to the pub/sub trigger by going to your google cloud console in a browser,
navigating to the pub/sub products page, navigate to subscriptions and click on your pubsub-trigger.

You must then click edit, and check off enable authentication. Click the appropriate service account 
and paste in your environment variable MY_RUN_SERVICE into the optional audience field. You must now
scroll down and select update for the changes to take place. 

## Test

Get a response from your Cloud Run Service

```sh
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" $MY_RUN_SERVICE
```

Test your Cloud Run service by publishing a message to the topic: 

```sh
gcloud pubsub topics publish my-topic --message="Hello there"
```

You may observe the Run service receiving an event in Cloud Logging.

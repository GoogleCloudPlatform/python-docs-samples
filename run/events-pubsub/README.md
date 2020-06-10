# Events for Cloud Run – Pub/Sub tutorial

This sample shows how to create a service that processes authenticated Pub/Sub 
messages.

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

When asked if you want to allow unauthenticated invocations, say no 

Retrieve container URL from the gcloud run deploy command executed above and 
store it as seen below

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

Then store the pubsub subscription name into a variable for future commands. 
First list your subscriptions by using the following command:

```sh
basename -a $(gcloud pubsub subscriptions list --format 'value(name)')
```

Grab a subscription name and save it to a variable SUBSCRIPTION

```sh
SUBSCRIPTION=<pubsub_subscription_name>
```

Finally we need to enable authenticated calls to the pub/sub trigger otherwise
cloud run will reject the incoming unauthenticated pubsub trigger requests. 

First we must choose a service account. You can list your service accounts via

```sh
gcloud iam service-accounts list
```

Choose an email and save it to a variable

```sh
SERVICE_ACCOUNT=<service_account_email>
```

Update pubsub subscription by doing the following:

```sh
gcloud pubsub subscriptions update $SUBSCRIPTION \
--push-auth-service-account=$SERVICE_ACCOUNT \
--push-auth-token-audience=$MY_RUN_SERVICE \
--push-endpoint=$(gcloud pubsub subscriptions describe $SUBSCRIPTION --format \
'value(pushConfig.pushEndpoint)')
```

In future versions of gcloud you won't need to use the --push-endpoint flag

## Test

Get a response from your Cloud Run Service using the following curl command.
Please note that the string "V29ybGQ=" is simply the word "World" encoded using
base64 encoding. All pubsub events have a base64 encoded message.data field.

```sh
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
--data '{"message": {"data": "V29ybGQ="}}' \
--header "Content-Type: application/json" $MY_RUN_SERVICE 
```

If everything is working you should have received a response of 
"Hello World!"

Now let's try sending an event using pubsub using the following gcloud command:

```sh
gcloud pubsub topics publish my-topic --message="John Doe"
```

You may use the following command to view and search through logs for all 
responses containing the textPayload of `Hello {name}!`

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=cloudrun-events-pubsub" --project \
$(gcloud config get-value project) --limit 100 | grep Hello
```

If the pubsub trigger was setup successfully, you should have seen 
Hello John Doe somewhere in the above output.

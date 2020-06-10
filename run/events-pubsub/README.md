# Events for Cloud Run – Pub/Sub tutorial

This sample shows how to create a service that processes Authenticated Pub/Sub 
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

Finally we need to enable authenticated calls to the pub/sub trigger otherwise
cloud run will reject the incoming unauthenticated pubsub trigger requests. 

via command line

```sh
gcloud pubsub subscriptions update my-topic \
--push-auth-service-account <iam-email>\
--push-auth-token-audience $MY_RUN_SERVICE
```

via google cloud console 

1. Login to google cloud console.
2. Navigate to the pub/sub products page, and select subscriptions from the left 
side tab bar.
3. Click on your pubsub-trigger then click edit.
4. Check off enable authentication.
5. Select the appropriate service account and paste in the value for
your environment variable MY_RUN_SERVICE into the optional audience field.  
6. Scroll down and click update for the changes to take place. 

## Test

Get a response from your Cloud Run Service using the following curl command.
Also note the string "V29ybGQ=" is simply the word "World" encoded using base64
encoding. All pubsub messages encode the message.data field using base64 
encoding

```sh
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
--data '{"message": {"data": "V29ybGQ="}}' \
--header "Content-Type: application/json" $MY_RUN_SERVICE 
```

If everything is working you should have received a response of "Hello World!"

Now let's try sending an event using pubsub using the following gcloud command:

```sh
gcloud pubsub topics publish my-topic --message="John Doe"
```

You may use this command to view and search through logs for all responses 
containing the textPayload of `Found message {name}!`

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=cloudrun-events-pubsub" --project \
$(gcloud config get-value project) --limit 100 | grep Hello
```

If the pubsub trigger was setup successfully, you should have seen 
Hello John Doe somewhere in the above output.

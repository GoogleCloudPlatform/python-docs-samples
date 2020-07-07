# Events for Cloud Run on Anthos – GCS tutorial

This sample shows how to create a service that processes GCS events. We assume
that you have a GKE cluster created with Events for Cloud Run enabled.

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
MY_GCS_BUCKET=gcs-bucket-$(gcloud config get-value project)
MY_CLUSTER_NAME=events-cluster
MY_CLUSTER_LOCATION=us-central1-c
```

## Quickstart

Set cluster name, location and platform:

```sh
gcloud config set run/cluster ${MY_CLUSTER_NAME}
gcloud config set run/cluster_location ${MY_CLUSTER_LOCATION}
gcloud config set run/platform gke
```

Deploy your Cloud Run service:

```sh
gcloud builds submit \
 --tag gcr.io/$(gcloud config get-value project)/$MY_RUN_CONTAINER
gcloud run deploy $MY_RUN_SERVICE \
 --image gcr.io/$(gcloud config get-value project)/$MY_RUN_CONTAINER
```

Create a bucket:

```sh
gsutil mb -p $(gcloud config get-value project) -l \
us-central1 gs://"$MY_GCS_BUCKET"
```

Before creating a trigger, you need to give the default service account for
Cloud Storage permission to publish to Pub/Sub.

Find the Service Account that Cloud Storage uses to publish
to Pub/Sub. You can use the steps outlined in [Cloud Console or the JSON
API](https://cloud.google.com/storage/docs/getting-service-account). Assume the
service account you found from above was
`service-XYZ@gs-project-accounts.iam.gserviceaccount.com`, set this to an
environment variable:

```sh
export GCS_SERVICE_ACCOUNT=service-XYZ@gs-project-accounts.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
--member=serviceAccount:${GCS_SERVICE_ACCOUNT} \
--role roles/pubsub.publisher
```

Create Cloud Storage trigger:

```sh
gcloud alpha events triggers create $MY_GCS_TRIGGER \
--target-service $MY_RUN_SERVICE \
--type=com.google.cloud.storage.object.finalize \
--parameters bucket=$MY_GCS_BUCKET
```

## Test

Test your Cloud Run service by uploading a file to the bucket:

```sh
echo "Hello World" > random.txt
gsutil cp random.txt gs://$MY_GCS_BUCKET/random.txt
```

Observe the Cloud Run service printing upon receiving an event in 
Cloud Logging:

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=$MY_RUN_SERVICE" --project \
$(gcloud config get-value project) --limit 30 --format 'value(textPayload)'
```

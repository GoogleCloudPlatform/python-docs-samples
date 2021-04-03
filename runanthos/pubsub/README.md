# Cloud Run for Anthos Pub/Sub Tutorial Sample

This sample shows how to create a service that processes Pub/Sub messages.

Use it with the [Cloud Pub/Sub with Cloud Run for Anthos tutorial](http://cloud.google.com/anthos/run/docs/tutorials/pubsub).

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/pubsub/README.md

## Build

```
docker build --tag pubsub-tutorial:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 pubsub-tutorial:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

_Note: [set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/tutorials/pubsub#setting-up-gcloud) before you begin._

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/pubsub-tutorial

# Deploy to Cloud Run for Anthos
gcloud run deploy pubsub-tutorial \
    --platform=managed \
    --image gcr.io/${GOOGLE_CLOUD_PROJECT}/pubsub-tutorial
```

# Timeseries classification

## TODO: add a README at the top level directory

ℹ️ The bucket _must_ be in the same region where the Vertex AI job runs.

```sh
# Google Cloud resources
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"
export REGION="us-central1"
```

## Uploading the data into Cloud Storage

```sh
# TODO: git clone
# TODO: gsutil -m cp ...
```

## Building the container image

```sh
gcloud builds submit . --tag="gcr.io/$PROJECT/samples/global-fishing-watch:latest"
```

## Deploying to Cloud Run

https://docs.gunicorn.org/en/stable/settings.html

```sh
gcloud run deploy "global-fishing-watch" \
    --image="gcr.io/$PROJECT/samples/global-fishing-watch:latest" \
    --command="gunicorn" \
    --args="--threads=8,--timeout=0,main:app" \
    --region="$REGION" \
    --no-allow-unauthenticated
```

```sh
export SERVICE_URL=$(gcloud run services describe "global-fishing-watch" \
    --region="$REGION" \
    --format="get(status.url)")
```

https://cloud.google.com/run/docs/authenticating/overview

## Creating the datasets

```sh
curl "$SERVICE_URL/create-datasets" \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

## Training the model

```sh
curl "$SERVICE_URL/train-model" \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

## Getting predictions

```sh
curl "$SERVICE_URL/predict" \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

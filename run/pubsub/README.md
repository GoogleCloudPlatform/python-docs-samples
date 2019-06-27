# Cloud Run Pub/Sub Tutorial Sample

This sample shows how to create a service that processes Pub/Sub messages.

Use it with the [Cloud Pub/Sub with Cloud Run tutorial](http://cloud.google.com/run/docs/tutorials/pubsub).

## Build

```
docker build --tag pubsub-tutorial:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 pubsub-tutorial:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

```
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/pubsub-tutorial
gcloud alpha run deploy pubsub-tutorial --image gcr.io/${GOOGLE_CLOUD_PROJECT}/pubsub-tutorial
```

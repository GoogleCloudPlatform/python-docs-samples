# Cloud Run Deployment Previews

This code creates a [Cloud Builder](https://cloud.google.com/cloud-build/docs/cloud-builders) 
to implement deployment previews in Cloud Run. It is designed to work with the Cloud Build 
configurations in `cloudbuild-configurations/`.

Use it with the [deployment previews tutorial](https://cloud.google.com/run/docs/tutorials/configure-deployment-previews).

## Build

```
docker build --tag deployment-previews:python .
```

## Run Locally

```
docker run --rm deployment-previews
```

## Test

```
pytest
```

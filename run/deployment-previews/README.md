# Cloud Run Deployment Previews

This code creates a Cloud Builder to implement deployment previews in Cloud Run. It is designed to work with the Cloud Build configurations in `cloudbuild-configurations/`.

Read more about how to work with [deployment previews](https://cloud.google.com/run/tutorials/configure-deployment-previews).

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

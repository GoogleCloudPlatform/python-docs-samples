# Cloud Run for Anthos Hello World Sample

This sample shows how to deploy a Hello World application to Cloud Run for Anthos.

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/helloworld/README.md

## Build

```
docker build --tag helloworld:python .
```

## Run Locally

```
docker run --rm -p 8080:8080 -e PORT=8080 helloworld:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

_Note: [set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/setup#configuring_default_settings_for_gcloud) before you begin._

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/helloworld

# Deploy to Cloud Run for Anthos
gcloud run deploy helloworld \
    --platform=managed \
    --image gcr.io/${GOOGLE_CLOUD_PROJECT}/helloworld
```

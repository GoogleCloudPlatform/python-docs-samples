# Cloud Run for Anthos Local Troubleshooting Sample

This sample presents broken code in need of troubleshooting.

Troubleshoot this code by following the [Local Container Troubleshooting Tutorial](http://cloud.google.com/anthos/run/docs/tutorials/local-troubleshooting).

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/hello-broken/README.md

## Build

```
docker build --tag hello-broken:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 hello-broken:python
```

## Test

```
nox -s "py36(sample='./run/hello-broken')"
```

_Note: you may need to install `nox` using `pip install nox`._

## Deploy

_Note: [set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/setup#configuring_default_settings_for_gcloud) before you begin._

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/hello-broken

# Deploy to Cloud Run for Anthos
gcloud run deploy hello-broken \
    --platform=managed \
    --image gcr.io/${GOOGLE_CLOUD_PROJECT}/hello-broken 
```

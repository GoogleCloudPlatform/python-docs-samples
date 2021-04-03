# Cloud Run for Anthos System Package Sample

This sample shows how to use a CLI tool installed as a system package as part of a web service.

Use it with the [Using system packages tutorial](https://cloud.google.com/anthos/run/docs/tutorials/system-packages).

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/system-package/README.md

## Build

```
docker build --tag graphviz:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 graphviz:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

_Note: [set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/tutorials/system-packages#setting-up-gcloud) before you begin._

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/graphviz

# Deploy to Cloud Run for Anthos
gcloud run deploy graphviz \
    --platform=managed \
    --image gcr.io/${GOOGLE_CLOUD_PROJECT}/graphviz
```

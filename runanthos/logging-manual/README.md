# Cloud Run for Anthos Manual Logging Sample

This sample shows how to send structured logs to Stackdriver Logging.

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/logging-manual/README.md

## Build

```
docker build --tag logging-manual:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 logging-manual:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

_Note: [set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/setup) before you begin._

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/logging-manual

# Deploy to Cloud Run for Anthos
gcloud run deploy logging-manual \
    --platform=managed \
    --image gcr.io/${GOOGLE_CLOUD_PROJECT}/logging-manual \
    --set-env-vars GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
```

Read more about CRfA logging in the [Logging How-to Guide](https://cloud.google.com/anthos/run/docs/logging).

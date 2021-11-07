# Cloud Run Manual Logging Sample

This sample shows how to send structured logs to Stackdriver Logging.

[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_working_dir=run/logging-manual

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

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/logging-manual

# Deploy to Cloud Run
gcloud run deploy logging-manual \
--image gcr.io/${GOOGLE_CLOUD_PROJECT}/logging-manual \
--set-env-vars GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
```

Read more about Cloud Run logging in the [Logging How-to Guide](http://cloud.google.com/run/docs/logging).

For more details on how to work with this sample read the [Python Cloud Run Samples README](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/run)

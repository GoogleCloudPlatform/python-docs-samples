# Cloud Run System Package Sample

This sample shows how to use a CLI tool installed as a system package as part of a web service.

Use it with the [Using system packages tutorial](https://cloud.google.com/run/docs/tutorials/system-packages).


[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_working_dir=run/system-package

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

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/graphviz

# Deploy to Cloud Run
gcloud run deploy graphviz --image gcr.io/${GOOGLE_CLOUD_PROJECT}/graphviz
```

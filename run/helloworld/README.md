# Cloud Run Hello World Sample

This sample shows how to deploy a Hello World application to Cloud Run.

[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_working_dir=run/helloworld

## Build

* Set an environment variable with your GCP Project ID:

```
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>
```

* Use a [Buildpack](https://github.com/GoogleCloudPlatform/buildpacks) to build the container:

```sh
gcloud builds submit --pack image=gcr.io/${GOOGLE_CLOUD_PROJECT}/helloworld
```

## Run Locally

```sh
docker run --rm gcr.io/${GOOGLE_CLOUD_PROJECT}/helloworld
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

# Deploy to Cloud Run
gcloud run deploy helloworld --source .
```


For more details on how to work with this sample read the [Python Cloud Run Samples README](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/run)

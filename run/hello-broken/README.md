# Cloud Run Broken Sample

This sample presents broken code in need of troubleshooting. View [improved](main.py#L43) for a more stable implementation. 

Troubleshoot this code by following the [Local Container Troubleshooting Tutorial](http://cloud.google.com/run/docs/tutorials/local-troubleshooting).

[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_working_dir=run/hello-broken

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

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/hello-broken

# Deploy to Cloud Run
gcloud run deploy hello-broken \
--image gcr.io/${GOOGLE_CLOUD_PROJECT}/hello-broken 
```


For more details on how to work with this sample read the [Python Cloud Run Samples README](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/run)

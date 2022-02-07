# Cloud Run Sample

## Build

* Set an environment variable with your GCP Project ID:

```
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>
```

* Use a [Buildpack](https://github.com/GoogleCloudPlatform/buildpacks) to build the container:

```sh
gcloud builds submit --pack image=gcr.io/${GOOGLE_CLOUD_PROJECT}/logger-job
```

## Run Locally

```sh
docker run --rm gcr.io/${GOOGLE_CLOUD_PROJECT}/logger-job

# With environment variables 
docker run --rm -e FAIL_RATE=0.9 -e SLEEP_MS=1000 gcr.io/${GOOGLE_CLOUD_PROJECT}/logger-job
```

## Test

```sh
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

~coming soon~

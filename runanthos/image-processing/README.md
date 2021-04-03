# Cloud Run for Anthos Image Processing Sample

This sample service applies [Cloud Storage](https://cloud.google.com/storage/docs)-triggered image processing with [Cloud Vision API](https://cloud.google.com/vision/docs) analysis and ImageMagick transformation.

Use it with the [Image Processing with Cloud Run for Anthos tutorial](https://cloud.google.com/anthos/run/docs/tutorials/image-processing).

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/image-processing/README.md

## Build

```
docker build --tag image-processing-tutorial:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 image-processing-tutorial:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

_Note: [set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/tutorials/image-processing#setting-up-gcloud) before you begin._

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/image-processing-tutorial

# Deploy to Cloud Run for Anthos
# Note: Replace <BLURRED_BUCKET_NAME> with the name of your Cloud Storage bucket.
gcloud run deploy image-processing-tutorial \
    --platform=managed \
    --image gcr.io/${GOOGLE_CLOUD_PROJECT}/image-processing-tutorial \
    --set-env-vars=BLURRED_BUCKET_NAME=<BLURRED_BUCKET_NAME>

```

## Environment Variables

Cloud Run for Anthos services can be [configured with Environment Variables](https://cloud.google.com/anthos/run/docs/configuring/environment-variables).
Required variables for this sample include:

* `BLURRED_BUCKET_NAME`: The Cloud Run for Anthos service will write blurred images to this Cloud Storage bucket.

## Maintenance Note

* The `image.py` file is copied from the [Cloud Functions ImageMagick sample `main.py`](../../functions/imagemagick/main.py). Region tags are changed.
* The requirements.txt dependencies used in the copied code should track the [Cloud Functions ImageMagick `requirements.txt`](../../functions/imagemagick/requirements.txt)


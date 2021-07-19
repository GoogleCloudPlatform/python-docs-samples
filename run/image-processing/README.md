# Cloud Run Image Processing Sample

This sample service applies [Cloud Storage](https://cloud.google.com/storage/docs)-triggered image processing with [Cloud Vision API](https://cloud.google.com/vision/docs) analysis and ImageMagick transformation.

Use it with the [Image Processing with Cloud Run tutorial](http://cloud.google.com/run/docs/tutorials/image-processing).

[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://deploy.cloud.run/?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&dir=run/image-processing

## Build

```
docker build --tag pubsub-tutorial:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 pubsub-tutorial:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

```
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/pubsub-tutorial

# Deploy to Cloud Run
gcloud run deploy pubsub-tutorial --image gcr.io/${GOOGLE_CLOUD_PROJECT}/pubsub-tutorial --set-env-vars=BLURRED_BUCKET_NAME=<BLURRED_BUCKET_NAME>

```

## Environment Variables

Cloud Run services can be [configured with Environment Variables](https://cloud.google.com/run/docs/configuring/environment-variables).
Required variables for this sample include:

* `INPUT_BUCKET_NAME`: The Cloud Run service will be notified of images uploaded to this Cloud Storage bucket. The service will then retrieve and process the image.
* `BLURRED_BUCKET_NAME`: The Cloud Run service will write blurred images to this Cloud Storage bucket.

## Maintenance Note

* The `image.py` file is copied from the [Cloud Functions ImageMagick sample `main.py`](../../functions/imagemagick/main.py). Region tags are changed.
* The requirements.txt dependencies used in the copied code should track the [Cloud Functions ImageMagick `requirements.txt`](../../functions/imagemagick/requirements.txt)


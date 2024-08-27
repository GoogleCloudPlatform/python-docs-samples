# Dataflow flex template: Getting started sample

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md).

## Create a Cloud Storage bucket

```sh
export BUCKET="your--bucket"
gsutil mb gs://$BUCKET
```

## create an Artifact Registry repository

```sh
export REGION="us-central1"
export REPOSITORY="your-repository"

gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION
```

## Build the template

```sh
export PROJECT="project-id"

gcloud dataflow flex-template build gs://$BUCKET/getting_started_py.json \
    --image-gcr-path "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/getting-started-py:latest" \
    --sdk-language "PYTHON" \
    --flex-template-base-image "PYTHON3" \
    --py-path "." \
    --metadata-file "metadata.json" \
    --env "FLEX_TEMPLATE_PYTHON_PY_FILE=getting_started.py" \
    --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=requirements.txt"
```

## Run the template

```sh
gcloud dataflow flex-template run "flex-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location "gs://$BUCKET/getting_started_py.json" \
    --region $REGION \
    --parameters output="gs://$BUCKET/output-"
```

## What's next?

For more information about building and running flex templates, see
📝 [Use Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates).


# Timeseries classification

## TODO: add a README at the top level directory

ℹ️ The bucket _must_ be in the same location where the Vertex AI job runs.

```sh
# Google Cloud resources
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"

export LOCATION="us-central1"
export STORAGE_DIR="samples/global-fishing-watch"
```

## Uploading the data into Cloud Storage

```sh
# TODO: git clone
# TODO: gsutil -m cp ...
```

## Building the container image

```sh
gcloud builds submit . --config="build.yaml"
```

## Creating the datasets with Dataflow

```sh
gcloud beta builds submit --no-source \
    --config="create_datasets.yaml" \
    --substitutions _BUCKET=$BUCKET,_LOCATION=$LOCATION
```

## Training the model in Vertex AI

```sh
# TODO: maybe change this to a Cloud Run config as well (?)
python run_training_job.py \
    --project "$PROJECT" \
    --bucket "$BUCKET" \
    --location "$LOCATION"
```

## TODO: Hyperparameter tuning

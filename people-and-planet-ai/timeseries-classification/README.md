# Timeseries classification

## TODO: add a README at the top level directory

```sh
# Google Cloud resources
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"

export REGION="us-central1"
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
    --substitutions _BUCKET=$BUCKET,_REGION=$REGION
```

## Training the model in Vertex AI

```sh
# TODO: have all the code in a single file (?) (how does Vertex AI handle requirements.txt?)

# specify baseOutputDirectory: https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#FIELDS.base_output_directory

python run_training_job.py
```

## TODO: Hyperparameter tuning

# Timeseries classification

## TODO: add a README at the top level directory

```sh
# Google Cloud resources
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"
export REGION="us-central1"

export STORAGE_DIR="gs://$BUCKET/samples/global-fishing-watch"
export IMAGE="gcr.io/$PROJECT/samples/global-fishing-watch:latest"

# Raw data and labels files.
export DATA_DIR="$STORAGE_DIR/data"
export LABELS_DIR="$STORAGE_DIR/labels"

# Training and evaluation datasets.
export TRAIN_DATA_DIR="$STORAGE_DIR/datasets/train"
export EVAL_DATA_DIR="$STORAGE_DIR/datasets/eval"

```

## Uploading the data into Cloud Storage

```sh
# TODO: git clone
# TODO: gsutil -m cp ...
```

## Creating the datasets with Dataflow

```sh
# TODO: move everything into a Docker container
# TODO: move this into a create-dataset.yaml file
python create_dataset.py \
    --data-files "$DATA_DIR/*.npz" \
    --label-files "$LABELS_DIR/*.csv" \
    --train-data-dir "$TRAIN_DATA_DIR" \
    --eval-data-dir "$EVAL_DATA_DIR" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --temp_location "gs://$BUCKET/temp" \
    --region "us-central1" \
    --setup_file "./setup.py"
```

## Training the model in Vertex AI

```sh
# TODO: have all the code in a single file (?) (how does Vertex AI handle requirements.txt?)

# specify baseOutputDirectory: https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#FIELDS.base_output_directory
```

## TODO: Hyperparameter tuning

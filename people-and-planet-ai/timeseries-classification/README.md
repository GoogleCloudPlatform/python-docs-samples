# Timeseries classification

## TODO: add a README at the top level directory.

```sh
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"
export REGION="us-central1"
```

## Creating the datasets

```sh
python create_dataset.py \
    --input-data "gs://$BUCKET/global-fishing-watch/data/*.npz" \
    --input-labels "gs://$BUCKET/global-fishing-watch/data/labels/*.csv" \
    --output-datasets-path "datasets"
```

```sh
python create_dataset.py \
    --input-data "gs://$BUCKET/global-fishing-watch/data/252626663422393.npz" \
    --input-labels "gs://$BUCKET/global-fishing-watch/data/labels/*.csv" \
    --output-datasets-path "gs://$BUCKET/global-fishing-watch/datasets" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --temp_location "gs://$BUCKET/global-fishing-watch/temp" \
    --region "us-central1" \
    --requirements_file "./requirements.txt"
    --setup_file "./setup.py"
```

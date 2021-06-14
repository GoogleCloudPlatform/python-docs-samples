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
    --output-path-prefix "gs://$BUCKET/global-fishing-watch/dataset" \
    --runner DataflowRunner \
    --project "$PROJECT" \
    --region "$REGION" \
    --temp_location "gs://$BUCKET/temp"

python trainer.py
```

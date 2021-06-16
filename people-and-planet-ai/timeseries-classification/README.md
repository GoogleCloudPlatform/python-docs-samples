# Timeseries classification

## TODO: add a README at the top level directory

```sh
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"
export REGION="us-central1"
```

## Creating the datasets

```sh
python create_dataset.py \
    --data-files "gs://$BUCKET/global-fishing-watch/data/252626663422393.npz" \
    --label-files "gs://$BUCKET/global-fishing-watch/data/labels/*.csv" \
    --train-data-dir "/tmp/datasets/train" \
    --eval-data-dir "/tmp/datasets/eval"
```

```sh
python create_dataset.py \
    --data-files "gs://$BUCKET/global-fishing-watch/data/*.npz" \
    --label-files "gs://$BUCKET/global-fishing-watch/data/labels/*.csv" \
    --train-data-dir "gs://$BUCKET/global-fishing-watch/datasets/train" \
    --eval-data-dir "gs://$BUCKET/global-fishing-watch/datasets/eval" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --temp_location "gs://$BUCKET/global-fishing-watch/temp" \
    --region "us-central1" \
    --setup_file "./setup.py"
```

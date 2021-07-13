# Timeseries classification

## TODO: add a README at the top level directory

ℹ️ The bucket _must_ be in the same region where the Vertex AI job runs.

```sh
# My Google Cloud resources.
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"
export REGION="us-central1"

export STORAGE_PATH="gs://$BUCKET/samples/global-fishing-watch"
export CONTAINER_IMAGE="gcr.io/$PROJECT/samples/global-fishing-watch"
```

## Uploading the data into Cloud Storage

```sh
# Install Git Large File Storage.
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.python.sh | bash
apt-get install -y git-lfs
git lfs install

# Clone the Global Fishing Watch training-data repository.
git clone https://github.com/GlobalFishingWatch/training-data.git ~/training-data

# Copy the data files and labels into Cloud Storage.
gsutil -mq cp -rn ~/training-data/data/tracks ${STORAGE_PATH}/data
gsutil -mq cp -rn ~/training-data/data/time-ranges ${STORAGE_PATH}/labels
```

## Deploying to Cloud Run

```sh
# Build the container image.
gcloud builds submit . --tag="${CONTAINER_IMAGE}"
```

```sh
# Deploy the image with Cloud Run.
gcloud run deploy "global-fishing-watch" \
    --image="${CONTAINER_IMAGE}" \
    --command="gunicorn" \
    --args="--threads=8,--timeout=0,main:app" \
    --region="${REGION}" \
    --memory="1G" \
    --set-env-vars "PROJECT=${PROJECT}" \
    --set-env-vars "STORAGE_PATH=${STORAGE_PATH}" \
    --set-env-vars "REGION=${REGION}" \
    --set-env-vars "CONTAINER_IMAGE=${CONTAINER_IMAGE}" \
    --no-allow-unauthenticated
```

```sh
export SERVICE_URL=$(gcloud run services describe "global-fishing-watch" \
    --region="$REGION" \
    --format="get(status.url)")
echo "SERVICE_URL=${SERVICE_URL}"

export ACCESS_TOKEN=$(gcloud auth print-identity-token)
echo "ACCESS_TOKEN=${ACCESS_TOKEN}"
```

```sh
# Make sure we can make authorized calls to our service.
curl "${SERVICE_URL}/ping" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"x": 42, "y": "Hello world!"}'
```

## Creating the datasets

```sh
curl "${SERVICE_URL}/create-datasets" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{}'
```

## Training the model

```sh
curl "${SERVICE_URL}/train-model" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"train_steps": 10000, "eval_steps": 1000}'
```

## Getting predictions

```sh
# TODO
```

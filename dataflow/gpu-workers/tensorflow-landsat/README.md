# Workers with GPUs

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/gpu-workers/README.md)

📝 Tutorial: [Processing Landsat satellite images with GPUs](https://cloud.google.com/dataflow/docs/samples/satellite-images-gpus)

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md), and additionally:

* Use or [create a Cloud Storage bucket](https://console.cloud.google.com/storage/create-bucket).

Finally, save your resource names in environment variables.

```sh
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-bucket-name"
```

## Building the Docker image

We use Cloud Build to build the container image for the workers.

```sh
gcloud builds submit --config build.yaml
```

## Running the Dataflow job with GPUs

We use Cloud Build to run the Dataflow job.
We launch the job using the worker image to make sure the job launches
with the same Python version as the workers.

```sh
export OUTPUT_PATH="gs://$BUCKET/samples/dataflow/landsat/"
export REGION="us-central1"
export WORKER_ZONE="us-central1-f"
export GPU_TYPE="nvidia-tesla-t4"

gcloud beta builds submit \
    --config run.yaml \
    --substitutions _OUTPUT_PATH=$OUTPUT_PATH,_REGION=$REGION,_WORKER_ZONE=$WORKER_ZONE,_GPU_TYPE=$GPU_TYPE \
    --no-source
```

> ℹ️ Make sure the GPU type you choose is available in the worker zone for the job.
> For more information, see [GPU availability](https://cloud.google.com/dataflow/docs/resources/locations#gpu_availability).

# PyTorch GPU minimal pipeline

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md).

Finally, save your resource names in environment variables.

```sh
export PROJECT=$(gcloud config get-value project)
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
export REGION="us-central1"
export GPU_TYPE="nvidia-tesla-t4"

gcloud beta builds submit \
    --config run.yaml \
    --substitutions _REGION=$REGION,_GPU_TYPE=$GPU_TYPE \
    --no-source
```

> ℹ️ Make sure the GPU type you choose is available in the worker zone for the job.
> For more information, see [GPU availability](https://cloud.google.com/dataflow/docs/resources/locations#gpu_availability).

## What's next?

For a more complete example, take a look at
📝 [Processing Landsat satellite images with GPUs](https://cloud.google.com/dataflow/docs/samples/satellite-images-gpus).

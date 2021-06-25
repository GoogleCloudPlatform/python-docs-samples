# PyTorch GPU minimal pipeline

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md).

## Building the Docker image

We use
[Cloud Build](https://cloud.google.com/build)
to build the container image for the workers and save it in
[Container Registry](https://cloud.google.com/container-registry/).

```sh
gcloud builds submit --config build.yaml
```

## Running the Dataflow job with GPUs

We use Cloud Build to run the [Dataflow](https://cloud.google.com/dataflow) job.

> ℹ️ We launch the job using the worker image to make sure the job launches
> with the same Python version as the workers and all the dependencies installed.

```sh
export REGION="us-central1"
export GPU_TYPE="nvidia-tesla-t4"

gcloud builds submit \
    --config run.yaml \
    --substitutions _REGION=$REGION,_GPU_TYPE=$GPU_TYPE \
    --no-source
```

## What's next?

For a more complete example, take a look at
📝 [Processing Landsat satellite images with GPUs](https://cloud.google.com/dataflow/docs/samples/satellite-images-gpus).

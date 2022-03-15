# Ubuntu custom container

This sample runs a Dataflow pipeline where the workers use a custom image based on the official [`ubuntu`](https://hub.docker.com/_/ubuntu) image.

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md).

You will also need:
* A Cloud Storage bucket, click [here to create one](https://console.cloud.google.com/storage/create-bucket) if needed.

```sh
export PROJECT=$(gcloud config get-value project)
export BUCKET="my-cloud-storage-bucket"
```

> ℹ️ Make sure your `BUCKET` name does _not_ include the `gs://` prefix.

## Building the Docker image

We use
[Cloud Build](https://cloud.google.com/build)
to build the container image for the workers and save it in
[Container Registry](https://cloud.google.com/container-registry/).

```sh
export IMAGE=gcr.io/$PROJECT/samples/dataflow-ubuntu:latest

gcloud builds submit . --tag=$IMAGE
```

## Running the Dataflow job

** ⚠️ Make sure you launch the pipeline using the same Python version as the
container image.**

> We can launch the pipeline from the same container, for an example on
> how to do that with Cloud Build, see the
> [`tensorflow-minimal`](../../gpu-examples/tensorflow-minimal) example

```sh
# Choose the location where you want to run your Dataflow job.
# For a list of all supported locations, see:
#   https://cloud.google.com/dataflow/docs/resources/locations
export REGION="us-central1"

python main.py \
    --runner DataflowRunner \
    --project $PROJECT \
    --region $REGION \
    --temp_location gs://$BUCKET/samples/dataflow-ubuntu \
    --sdk_container_image=$IMAGE
```

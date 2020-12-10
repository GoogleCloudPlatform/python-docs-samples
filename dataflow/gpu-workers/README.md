# Workers with GPUs

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/gpu-workers/README.md)

This tutorial shows you how to use GPUs on Cloud Dataflow to process
[Landsat satellite images](https://cloud.google.com/storage/docs/public-datasets/landsat)
and render them as JPEG files.

## Before you begin

Follow the
[Getting started with Cloud Dataflow](../README.md)
page, and make sure you have a Google Cloud project with billing enabled
and a *service account JSON key* set up in your `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
Additionally, for this sample you need the following:

1. [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=cloudbuild.googleapis.com)
    Cloud Build.

1. Create a Cloud Storage bucket.

   ```sh
   export BUCKET=your-gcs-bucket
   gsutil mb gs://$BUCKET
   ```

1. Clone the `python-docs-samples` repository.

    ```sh
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

1. Navigate to the sample code directory.

   ```sh
   cd python-docs-samples/dataflow/gpu-workers
   ```

1. Create a Python 3.7 virtual environment and activate it.

    ```sh
    python3.7 -m venv env
    source env/bin/activate
    ```

    > Once you are done with this tutorial, you can run `deactivate` to exit the virtualenv.

1. Install the sample requirements.

    ```sh
    pip install -r requirements.txt
    ```

## Building the Docker image

Cloud Build allows you to
[build a Docker image using a `Dockerfile`](https://cloud.google.com/cloud-build/docs/quickstart-docker#build_using_dockerfile).
and save it into
[Container Registry](https://cloud.google.com/container-registry/),
where the image is accessible to other Google Cloud products.

```sh
export IMAGE="gcr.io/$PROJECT/samples/dataflow/tensorflow-gpu:latest"

# Build the image into Container Registry, this is roughly equivalent to:
#   gcloud auth configure-docker
#   docker image build -t $IMAGE .
#   docker push $IMAGE
gcloud builds submit -t $IMAGE .
```

## Running in Dataflow with GPUs

For this sample, the only required command line argument is `--output-path-prefix`.
To run in Dataflow, the `--output-path-prefix` must be a Cloud Storage path starting with `gs://`.

To run with GPUs, we need to configure:

- `--worker_harness_container_image` to the Container Registry path of our image.
- `--worker_zone` to a [zone](/compute/docs/gpus#introduction) that supports the GPU type you want.
- `--experiments` to configure the `worker_accelerator` options.
- `--experiments` to `"use_runner_v2"`.

```sh
export REGION="us-central1"
export WORKER_ZONE="$REGION-a"
export GPU_TYPE="nvidia-tesla-v100"
export MACHINE_TYPE="custom-1-13312-ext"

python landsat_view.py \
    --output-path-prefix "gs://$BUCKET/samples/dataflow/landsat/" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --region "$REGION" \
    --machine_type "$MACHINE_TYPE" \
    --worker_harness_container_image "$IMAGE" \
    --worker_zone "$WORKER_ZONE" \
    --experiments "worker_accelerator=type=$GPU_TYPE,count=1,install-nvidia-driver" \
    --experiments "use_runner_v2"

```

> ℹ️ The image uses CUDA version 10.1 with cuDNN version 7 since those are the
> versions compatible with the Tensorflow version we are using.
>
> For a list of all the compatible versions, see the
> [Tensorflow tested build configurations](https://www.tensorflow.org/install/source#gpu) page.

## View your results

We can check the output JPEG files using
[`gsutil`](https://cloud.google.com/storage/docs/gsutil).

```sh
# To list the files with details.
gsutil ls -lh "gs://$BUCKET/samples/dataflow/landsat/"
```

To view the images, we can copy the files into our local directory and then
open them with the image viewer of your choice.

```sh
gsutil -m cp "gs://$BUCKET/samples/dataflow/landsat/*" outputs/
```

## Cleaning up

After you've finished this tutorial, you can clean up the resources you created on Google Cloud so you won't be billed for them in the future. The following sections describe how to delete or turn off these resources.

### Clean up the sample resources

1. Delete the output files from Cloud Storage.

    ```sh
    gsutil -m rm "gs://$BUCKET/samples/dataflow/landsat"
    ```

1. Delete the container image from Container Registry.

    ```sh
    gcloud container images delete $IMAGE --force-delete-tags
    ```

### Clean up Google Cloud project resources

1. Delete the Cloud Storage bucket, this alone does not incur any charges.

    > ⚠️ The following command also deletes all objects in the bucket.
    > These objects cannot be recovered.
    >
    > ```sh
    > gsutil rm -r gs://$BUCKET
    > ```

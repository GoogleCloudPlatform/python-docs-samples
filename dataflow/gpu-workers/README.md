# Workers with GPUs

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/gpu-workers/README.md)

This sample demonstrate how to use
[cryptographic encryption keys](https://cloud.google.com/kms/)
for the I/O connectors in an
[Apache Beam](https://beam.apache.org) pipeline.
For more information, see the
[Using customer-managed encryption keys](https://cloud.google.com/dataflow/docs/guides/customer-managed-encryption-keys)
docs page.

## Before you begin

Follow the
[Getting started with Google Cloud Dataflow](../README.md)
page, and make sure you have a Google Cloud project with billing enabled
and a *service account JSON key* set up in your `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
Additionally, for this sample you need the following:

1. [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery,cloudkms.googleapis.com):
    BigQuery and Cloud KMS API.

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

    > Once you are done, you can deactivate the virtualenv and go back to your global Python environment by running `deactivate`.

1. Install the sample requirements.

    ```sh
    pip install -U -r requirements.txt
    ```

## Running a Dataflow job using workers with GPUs

* [landsat_images.py](landsat_images.py)

Download cuDNN.
Download cuDNN from the [Nvidia website](https://developer.nvidia.com/cudnn) into the sample directory.

> Must be **exactly** version 10.1 for Linux x86: `cudnn-10.1-linux-x64-v8.0.4.30.tgz`
>
> For more information about the supported CUDA versions, see the
> [TensorFlow GPU support](https://www.tensorflow.org/install/gpu) page.

Building the Docker image.

Cloud Build allows you to
[build a Docker image using a `Dockerfile`](https://cloud.google.com/cloud-build/docs/quickstart-docker#build_using_dockerfile).
and saves it into
[Container Registry](https://cloud.google.com/container-registry/),
where the image is accessible to other Google Cloud products.

```sh
export IMAGE="gcr.io/$PROJECT/samples/dataflow/python-gpu:latest"

# Build the image into Container Registry, this is roughly equivalent to:
#   gcloud auth configure-docker
#   docker image build -t $IMAGE .
#   docker push $IMAGE
gcloud builds submit -t $IMAGE .
```

Running in Dataflow with GPUs.

Notes and current limitations:

* Must use a machine type with 1 core due to the way Tensorflow uses the GPU memory
* Won't run in an n1-standard-1 because it needs more memory, so we use a custom machine type with 1 core and 13 GB (13 * 1024 MB) of memory `custom-1-13312-ext`.
* Only specific GPUs are available in specific certain zones, `us-central1-a` has `nvidia-tesla-v100` (we need to provide a list of zones with available GPUs, plus pricing)

```sh
# Run WITH GPUs
export IMAGE="gcr.io/$PROJECT/samples/dataflow/python-gpu:latest"
export REGION="us-central1"
export WORKER_ZONE="$REGION-a"
export GPU_TYPE="nvidia-tesla-v100"
export MACHINE_TYPE="custom-1-13312-ext"

# Run WITH GPUs
export PROJECT="google.com:deft-testing-integration"
export BUCKET="dcavazos-dataflow-testing"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/creds/deft-testing-integration.json"
export IMAGE="gcr.io/google.com/deft-testing-integration/dcavazos/python-gpu:latest"
export REGION="us-central1"
export WORKER_ZONE="$REGION-a"
export GPU_TYPE="nvidia-tesla-v100"
export MACHINE_TYPE="custom-1-13312-ext"

# Run locally
python landsat_view.py \
    --output-path-prefix "gs://$BUCKET/samples/dataflow/landsat/" \
    --experiments "use_runner_v2"

# Run in Dataflow *** NO GPUS, CPU only ***
python landsat_view.py \
    --output-path-prefix "gs://$BUCKET/samples/dataflow/landsat/" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --region "$REGION" \
    --worker_harness_container_image "$IMAGE" \
    --worker_zone "$WORKER_ZONE" \
    --machine_type "$MACHINE_TYPE" \
    --dataflow_endpoint "https://dataflow-valentyn-staging.sandbox.googleapis.com/" \
    --autoscaling_algorithm NONE \
    --num_workers 5 \
    --experiments "use_runner_v2"

# Run with GPUs in Valentyn's sandbox.
python landsat_view.py \
    --output-path-prefix "gs://$BUCKET/samples/dataflow/landsat/" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --region "$REGION" \
    --worker_harness_container_image "$IMAGE" \
    --worker_zone "$WORKER_ZONE" \
    --machine_type "$MACHINE_TYPE" \
    --dataflow_endpoint "https://dataflow-valentyn-staging.sandbox.googleapis.com/" \
    --experiments "worker_accelerator=type=$GPU_TYPE,count=1,install-nvidia-driver" \
    --autoscaling_algorithm NONE \
    --num_workers 5 \
    --experiments "use_runner_v2"

# Run in daily sandbox.
python landsat_view.py \
    --output-path-prefix "gs://$BUCKET/samples/dataflow/landsat/" \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --region "$REGION" \
    --worker_harness_container_image "$IMAGE" \
    --worker_zone "$WORKER_ZONE" \
    --machine_type "$MACHINE_TYPE" \
    --dataflow_endpoint "https://dataflow-daily.sandbox.googleapis.com/" \
    --experiments "worker_accelerator=type=$GPU_TYPE,count=1,install-nvidia-driver" \
    --experiments "use_runner_v2"

```

View results.

```sh
export BUCKET="dcavazos-dataflow-testing"

gsutil ls -lh gs://$BUCKET/samples/dataflow/landsat/

gsutil -m cp "gs://$BUCKET/samples/dataflow/landsat/*" outputs/
```

# Processing Landsat satellite images with GPUs

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/gpu-workers/README.md)

> ℹ️ This sample requires Apache Beam version 2.35 or higher.

📝 Tutorial: [Processing Landsat satellite images with GPUs](https://cloud.google.com/dataflow/docs/samples/satellite-images-gpus)

## Before you begin

Make sure you have followed the
[Dataflow setup instructions](../../README.md).

* Enable the Cloud Autoscaling API.

    <button><a href="https://console.cloud.google.com/flows/enableapi?apiid=autoscaling.googleapis.com">
        Click here to enable the API
    </a></button>

    Dataflow Prime uses the Cloud Autoscaling API to dynamically adjust memory.

    > ℹ️ For more information on Dataflow Prime, see the [Using Dataflow Prime](https://cloud.google.com/dataflow/docs/guides/enable-dataflow-prime#enable-prime) page in the documentation.

* Create a new Cloud Storage bucket or use an existing one for the output image files.

    <button><a href="https://console.cloud.google.com/storage/create-bucket">
        Click here to create a bucket
    </a></button>

    ```sh
    # Export an environment variable with your bucket name without the gs:// prefix.
    export BUCKET="your-cloud-storage-bucket"
    ```

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

For more information on the available GPU types per location, see the
[GPU availability](https://cloud.google.com/dataflow/docs/resources/locations#gpu_availability)
section in the documentation.

> ℹ️ We launch the job using the worker image to make sure the job launches
> with the same Python version as the workers and all the dependencies installed.

```sh
export JOB_NAME="tensorflow-landsat-$(date +%F-%H%M%S)"
export OUTPUT_PATH="gs://$BUCKET/samples/dataflow/landsat/output-images/"
export REGION="us-central1"
export GPU_TYPE="nvidia-tesla-t4"

gcloud builds submit \
    --config run.yaml \
    --substitutions _JOB_NAME=$JOB_NAME,_OUTPUT_PATH=$OUTPUT_PATH,_REGION=$REGION,_GPU_TYPE=$GPU_TYPE \
    --no-source
```

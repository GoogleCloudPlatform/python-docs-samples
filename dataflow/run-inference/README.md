# Streaming RunInference LLM

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/run-inference/README.md)

This sample shows how to run a [Large Language Model (LLM)](https://en.wikipedia.org/wiki/Large_language_model) in a streaming Dataflow pipeline.

## Before you begin

> 💡 Make sure you have followed the
[Dataflow setup instructions](../README.md).

```sh
# Make sure you have the following environment variables.
export PROJECT="my-google-cloud-project-id"
export BUCKET="my-cloud-storage-bucket"  # without the "gs://" prefix
export LOCATION="us-central1"  # or your location of choice
```

Create the following Pub/Sub topics:
* `messages`: For the input messages to send to the model.
* `responses`: For the model's responses.

```sh
export MESSAGES_TOPIC="projects/$PROJECT/topics/messages"
export RESPONSES_TOPIC="projects/$PROJECT/topics/responses"

# Create the Pub/Sub topics.
gcloud pubsub topics create $MESSAGES_TOPIC
gcloud pubsub topics create $RESPONSES_TOPIC
```

## Load the `state_dict`

LLMs can be **very large** models. Make sure the VMs you choose have enough memory to load them.
Larger models generally give better results, but require more memory and can be slower to run on CPUs.
You can [add GPUs](https://cloud.google.com/dataflow/docs/concepts/gpu-support) if you need faster responses.

| Model                                   | Parameters | Memory needed |
|-----------------------------------------|-----------:|--------------:|
| [`google/flan-t5-small`][flan-t5-small] | 80M        | > 320 MB      |
| [`google/flan-t5-base`][flan-t5-base]   | 250M       | > 1 GB        |
| [`google/flan-t5-large`][flan-t5-large] | 780M       | > 3.2 GB      |
| [`google/flan-t5-xl`][flan-t5-xl]       | 3B         | > 12 GB       |
| [`google/flan-t5-xxl`][flan-t5-xxl]     | 11B        | > 44 GB       |
| [`google/flan-ul2`][flan-ul2]           | 20B        | > 80 GB       |

> 💡 Larger models require larger VMs to run.

When running in Dataflow, Apache Beam's [`RunInference`](https://beam.apache.org/documentation/transforms/python/elementwise/runinference/) expects the model's  [`state_dict`](https://pytorch.org/tutorials/recipes/recipes/what_is_state_dict.html) to reside in Cloud Storage.

Because LLMs can be so large, save the `state_dict` as `float16` instead of the default `float32`.
With this configuration, each parameter uses 16 bits instead of 32 bits, making the `state_dict` half the size, which minimizes the time needed to load the model.
However, converting the `state_dict` from `float32` to `float16` means our VM has to fit _both_ into memory.

You can run smaller models locally if you have enough memory to load the model. You also need a fast internet connection to download the weights and to upload them to Cloud Storage.
If you're not running the model locally, launch a Vertex AI custom job to load the model for into an appropriately sized VM.
The minimum (and default) disk size for Vertex AI is 100 GB, but some models might require a larger disk.

The following table provides the minimum requirements to load a model's `state_dict`.

| Model name             | Memory needed | Machine type    | VM Memory | VM Disk |
|------------------------|---------------|-----------------|-----------|---------|
| `google/flan-t5-small` | > 480 MB      | `e2-standard-4` | 16 GB     | 100 GB  |
| `google/flan-t5-base`  | > 1.5 GB      | `e2-standard-4` | 16 GB     | 100 GB  |
| `google/flan-t5-large` | > 4.8 GB      | `e2-standard-4` | 16 GB     | 100 GB  |
| `google/flan-t5-xl`    | > 18 GB       | `e2-highmem-4`  | 32 GB     | 100 GB  |
| `google/flan-t5-xxl`   | > 66 GB       | `e2-highmem-16` | 128 GB    | 100 GB  |
| `google/flan-ul2`      | > 120 GB      | `e2-highmem-16` | 128 GB    | 150 GB  |

```sh
export MODEL_NAME="google/flan-t5-xl"
export MACHINE_TYPE="e2-highmem-4"
export DISK_SIZE_GB=100  # minimum is 100

python download_model.py vertex \
    --model-name="$MODEL_NAME" \
    --state-dict-path="gs://$BUCKET/run-inference/$MODEL_NAME.pt" \
    --job-name="Load $MODEL_NAME" \
    --project="$PROJECT" \
    --bucket="$BUCKET" \
    --location="$LOCATION" \
    --machine-type="$MACHINE_TYPE" \
    --disk-size-gb="$DISK_SIZE_GB"
```

## Run the pipeline

To run the pipeline in Dataflow, the model must fit into memory along with the rest of the memory used by each worker.

We use `--experiments="no_use_multiple_sdk_containers"` to make sure there's only one process per worker.
This ensures the model is only loaded once per worker, and we won't run out of memory.
`RunInference` shares the same model with multiple threads, so we don't have to limit the number of threads.

The following table shows the recommended machine types to run an inference pipeline.

| Model name             | Machine type    | VM Memory |
|------------------------|-----------------|-----------|
| `google/flan-t5-small` | `n2-highmem-2`  | 16 GB     |
| `google/flan-t5-base`  | `n2-highmem-2`  | 16 GB     |
| `google/flan-t5-large` | `n2-highmem-4`  | 32 GB     |
| `google/flan-t5-xl`    | `n2-highmem-4`  | 32 GB     |
| `google/flan-t5-xxl`   | `n2-highmem-8`  | 64 GB     |
| `google/flan-ul2`      | `n2-highmem-16` | 128 GB    |

```sh
export MODEL_NAME="google/flan-t5-xl"
export MACHINE_TYPE="n2-highmem-4"

# Launch the Datflow pipeline.
python main.py \
  --messages-topic="$MESSAGES_TOPIC" \
  --responses-topic="$RESPONSES_TOPIC" \
  --model-name="$MODEL_NAME" \
  --state-dict-path="gs://$BUCKET/run-inference/$MODEL_NAME.pt" \
  --runner="DataflowRunner" \
  --project="$PROJECT" \
  --temp_location="gs://$BUCKET/temp" \
  --region="$LOCATION" \
  --machine_type="$MACHINE_TYPE" \
  --requirements_file="requirements.txt" \
  --requirements_cache="skip" \
  --experiments="use_sibling_sdk_workers" \
  --experiments="no_use_multiple_sdk_containers"
```

> 💡 This pipeline is running with CPUs only.
> Larger models require more time to process each request, so you might want to enable GPUs.

## What's next?

- [Available machine types](https://cloud.google.com/compute/docs/general-purpose-machines)
- [VM instance pricing](https://cloud.google.com/compute/vm-instance-pricing).
- [Dataflow with GPUs](https://cloud.google.com/dataflow/docs/concepts/gpu-support)

[flan-t5-small]: https://huggingface.co/google/flan-t5-small
[flan-t5-base]: https://huggingface.co/google/flan-t5-base
[flan-t5-large]: https://huggingface.co/google/flan-t5-large
[flan-t5-xl]: https://huggingface.co/google/flan-t5-xl
[flan-t5-xxl]: https://huggingface.co/google/flan-t5-xxl
[flan-ul2]: https://huggingface.co/google/flan-ul2

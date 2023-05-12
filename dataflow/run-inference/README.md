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
* `messages`: For the input messages to send to the LLM model.
* `responses`: For the model's responses.

  <button onclick="https://console.cloud.google.com/cloudpubsub/topic/create">Click here to create a Pub/Sub topic</button>

```sh
export MESSAGES_TOPIC="projects/$PROJECT/topics/messages"
export RESPONSES_TOPIC="projects/$PROJECT/topics/responses"
```

## Loading the `state_dict`

LLMs can be **very large** models. Make sure the VMs you choose have enough memory to load them.
Larger models generally give better results, but require more memory and can be slower to run on CPUs.
You can add GPUs if you need faster responses.

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

Since LLMs can be so large, we want to save our `state_dict` as `float16` instead of the default `float32`.
This means each parameter uses 16 bits instead of 32 bits, making the `state_dict` be half the size, which minimizes the time to load the model.
However, converting the `state_dict` from `float32` to `float16` means our VM has to fit _both_ into memory.

For smaller models, you can run it locally as long as you have enough memory to load the model and a fast internet connection to download the weights and upload them to Cloud Storage.
Otherwise, we can launch a Vertex AI custom job to load it for us using a VM with the right size.
The minimum (and default) disk size for Vertex AI is 100 GB, but some models might require a larger disk.

Here's a table showing the minimum requirements to load a model's `state_dict`.

| Model name             | Memory needed | Machine type    | VM Memory | VM Disk |
|------------------------|---------------|-----------------|-----------|---------|
| `google/flan-t5-small` | > 480 MB      | `e2-standard-2` | 8 GB      | 100 GB  |
| `google/flan-t5-base`  | > 1.5 GB      | `e2-standard-2` | 8 GB      | 100 GB  |
| `google/flan-t5-large` | > 4.8 GB      | `e2-standard-2` | 8 GB      | 100 GB  |
| `google/flan-t5-xl`    | > 18 GB       | `e2-highmem-4`  | 32 GB     | 100 GB  |
| `google/flan-t5-xxl`   | > 66 GB       | `e2-highmem-16` | 128 GB    | 100 GB  |
| `google/flan-ul2`      | > 120 GB      | `e2-highmem-16` | 128 GB    | 150 GB  |

```sh
export MODEL_NAME="google/flan-t5-xl"
export MACHINE_TYPE="e2-highmem-4"
export DISK_SIZE_GB=100  # minimum is 100

python load-state-dict.py vertex \
    --model-name="$MODEL_NAME" \
    --state-dict-path="gs://$BUCKET/run-inference/$MODEL_NAME.pt" \
    --job-name="Load $MODEL_NAME" \
    --project="$PROJECT" \
    --bucket="$BUCKET" \
    --location="$LOCATION" \
    --machine-type="$MACHINE_TYPE" \
    --disk-size-gb="$DISK_SIZE_GB"
```

## Running the pipeline

To run the pipeline in Dataflow, we just need to make sure the model fits into memory.

Here's a table showing the minimum requirements to run an inference pipeline.

| Model name             | Memory needed | Machine type    | VM Memory |
|------------------------|---------------|-----------------|-----------|
| `google/flan-t5-small` | > 320 MB      | `n2-standard-2` | 8 GB      | 
| `google/flan-t5-base`  | > 1 GB        | `n2-standard-2` | 8 GB      |
| `google/flan-t5-large` | > 3.2 GB      | `n2-standard-2` | 8 GB      |
| `google/flan-t5-xl`    | > 12 GB       | `n2-highmem-2`  | 16 GB     |
| `google/flan-t5-xxl`   | > 44 GB       | `n2-highmem-8`  | 64 GB     |
| `google/flan-ul2`      | > 80 GB       | `n2-highmem-16` | 128 GB    |

```sh
export MODEL_NAME="google/flan-t5-xl"
export MACHINE_TYPE="n2-highmem-2"

python main.py \
  --messages-topic="$MESSAGES_TOPIC" \
  --responses-topic="$RESPONSES_TOPIC" \
  --state-dict-path="gs://$BUCKET/run-inference/$MODEL_NAME.pt" \
  --model-name="$MODEL_NAME" \
  --runner="DataflowRunner" \
  --project="$PROJECT" \
  --temp_location="gs://$BUCKET/temp" \
  --region="$LOCATION" \
  --machine_type="$MACHINE_TYPE"
```

## What's next?

[available machine types](https://cloud.google.com/compute/docs/general-purpose-machines)

[VM instance pricing](https://cloud.google.com/compute/vm-instance-pricing).

[flan-t5-small]: https://huggingface.co/google/flan-t5-small
[flan-t5-base]: https://huggingface.co/google/flan-t5-base
[flan-t5-large]: https://huggingface.co/google/flan-t5-large
[flan-t5-xl]: https://huggingface.co/google/flan-t5-xl
[flan-t5-xxl]: https://huggingface.co/google/flan-t5-xxl
[flan-ul2]: https://huggingface.co/google/flan-ul2

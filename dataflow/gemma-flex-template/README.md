# RunInference on Dataflow streaming with Gemma and Flex Templates

Gemma is a family of lightweight, state-of-the-art open models built from research and technology used to create the Gemini models.
You can use Gemma models in your Apache Beam inference pipelines with the `RunInference` transform.

This example demonstrates how to use a Gemma model running on Pytorch in a streaming Dataflow pipeline that has Pub/Sub sources and sinks. This pipeline
is deployed by using Flex Templates.

For more information about using RunInference, see [Get started with AI/ML pipelines](https://beam.apache.org/documentation/ml/overview/) in the Apache Beam documentation.

## Before you begin

Make sure you have followed the [Dataflow setup instructions](/dataflow/README.md).

Follow the steps in this section to create the necessary environment to run this workflow.

### Enable Google Cloud services

This workflow uses multiple Google Cloud products, including Dataflow, Pub/Sub, Google Cloud Storage, and Artifact Registry. Before you start the workflow, create a Google Cloud project that has the following services enabled:

* Dataflow
* Pub/Sub
* Compute Engine
* Cloud Logging
* Google Cloud Storage
* Google Cloud Storage JSON
* Cloud Build
* Datastore
* Cloud Resource Manager
* Artifact Registry

Using these services incurs billing charges.

Your Google Cloud project also needs to have Nvidia L4 GPU quota. For more information, see [GPU quota](https://cloud.google.com/compute/resource-usage#gpu_quota) in the Google Cloud documentation.

### Download and save the model

Save a version of the Gemma 2B model. Downloaded the model from [Kaggle](https://www.kaggle.com/models/google/gemma/pyTorch/1.1-2b-it). This download is a `.tar.gz` archive. Extract the archive into a directory and name it `pytorch_model`. 

### Create a cloud storage bucket

Click [here to create a GCS bucket](https://console.cloud.google.com/storage/create-bucket) or run the following commands:

```sh
export GCS_BUCKET="your--bucket"
gsutil mb gs://$GCS_BUCKET
```

Make sure your GCS bucket name does __not__ include the `gs://` prefix

### Create a custom container

To build a custom container, use Docker. This repository contains a Dockerfile that you can use to build your custom container. To build and push a container to Artifact Registry by using Docker or Cloud Build, follow the instructions in the [Build and push the image](https://cloud.google.com/dataflow/docs/guides/build-container-image#build_and_push_the_image) section of "Build custom container images for Dataflow" in the Google Cloud documentation.

### Create Pub/Sub topics for input and output

To create your Pub/Sub source and sink, follow the instructions in [Create a Pub/Sub topic](https://cloud.google.com/pubsub/docs/create-topic#pubsub_create_topic-Console) in the Google Cloud documentation. For this example, create two topics, one input topic and one output topic. Follow the instructions in [Create pull subscriptions](https://cloud.google.com/pubsub/docs/create-subscription) to create a pull subscription for each of the two topics you jsut created. The input subscription allows you to provide input to the pipeline, while the output subscription will allow you to see the output from the pipeline during and after execution.

## Code overview

This section provides details about the custom model handler and the formatting `DoFn` used in this example.

### Custom model handler
This example defines a custom model handler that loads the model. The model handler constructs a configuration object and loads the model's checkpoint from the local filesystem.
Because this approach differs from the PyTorch model loading process followed in the Beam PyTorch model handler, a custom implementation is necessary. 

To customize the behavior of the handler, implement the following methods: `load_model`, `validate_inference_args`, and `share_model_across_processes`.

The PyTorch implementation of the Gemma models has a `generate` method
that generates text based on a prompt. To route the prompts correctly, use this function in the `run_inference` function.

```py
class GemmaPytorchModelHandler(ModelHandler[str, PredictionResult,
                                            GemmaForCausalLM]):
    def __init__(self,
                 model_variant: str,
                 checkpoint_path: str,
                 tokenizer_path: str,
                 device: Optional[str] = 'cpu'):
        """ Implementation of the ModelHandler interface for Gemma-on-Pytorch
        using text as input.

        Example Usage::

          pcoll | RunInference(GemmaPytorchHandler())

        Args:
          model_variant: The Gemma model name.
          checkpoint_path: the path to a local copy of gemma model weights.
          tokenizer_path: the path to a local copy of the gemma tokenizer
          device: optional. the device to run inference on. can be either
            'cpu' or 'gpu', defaults to cpu. 
        """
        model_config = get_config_for_2b(
        ) if "2b" in model_variant else get_config_for_7b()
        model_config.tokenizer = tokenizer_path
        model_config.quant = 'quant' in model_variant
        model_config.tokenizer = tokenizer_path

        self._model_config = model_config
        self._checkpoint_path = checkpoint_path
        if device == 'GPU':
            logging.info("Device is set to CUDA")
            self._device = torch.device('cuda')
        else:
            logging.info("Device is set to CPU")
            self._device = torch.device('cpu')
        self._env_vars = {}

    def load_model(self) -> GemmaForCausalLM:
        """Loads and initializes a model for processing."""
        torch.set_default_dtype(self._model_config.get_dtype())
        model = GemmaForCausalLM(self._model_config)
        model.load_weights(self._checkpoint_path)
        model = model.to(self._device).eval()
        return model
```

### Formatting DoFn

The output from a keyed model handler is a tuple of the form `(key, PredictionResult)`. To format that output into a string before sending it to the answer Pub/Sub topic, use an extra `DoFn`.

```py
| "Format output" >> beam.Map(
    lambda response: json.dumps(
        {"input": response.example, "outputs": response.inference}
    )
)
```

## Build the Flex Template
Run the following code from the directory to build the Dataflow flex template.

- Replace `$GCS_BUCKET` with a Google Cloud Storage bucket.
- Set `SDK_CONTAINER_IMAGE` to the name of the Docker image created previously.
- `$PROJECT` is the Google Cloud project that you created previously. 

```sh
gcloud dataflow flex-template build gs://$GCS_BUCKET/config.json \
  --image $SDK_CONTAINER_IMAGE \
  --sdk-language "PYTHON" \
  --metadata-file metadata.json \
  --project $PROJECT
```

## Start the pipeline
To start the Dataflow streaming job, run the following code from the directory. Replace `$TEMPLATE_FILE`, `$REGION`, `$GCS_BUCKET`, `$INPUT_SUBSCRIPTION`, `$OUTPUT_TOPIC`, `$SDK_CONTAINER_IMAGE`, and `$PROJECT` with the Google Cloud project resources you created previously. Ensure that `$INPUT_SUBSCRIPTION` and `$OUTPUT_TOPIC` are the fully qualified subscription and topic names, respectively. It might take as much as 30 minutes for the worker to start up and to begin accepting messages from the input Pub/Sub topic. 

```sh
gcloud dataflow flex-template run "gemma-flex-`date +%Y%m%d-%H%M%S`" \
  --template-file-gcs-location $TEMPLATE_FILE \
  --region $REGION \
  --temp-location gs://$GCS_BUCKET/tmp \
  --staging-location gs://$GCS_BUCKET \
  --parameters messages_subscription=$INPUT_SUBSCRIPTION \
  --parameters responses_topic=$OUTPUT_TOPIC \
  --parameters device="GPU" \
  --parameters sdk_container_image=$SDK_CONTAINER_IMAGE \
  --additional-experiments "worker_accelerator=type:nvidia-l4;count:1;install-nvidia-driver" \
  --project $PROJECT \
  --worker-machine-type "g2-standard-4"
```

## Send a prompt to the model and check the response

In the Google Cloud console, navigate to the Pub/Sub topics page, and then select your input topic. On the **Messages** tab, click **Publish Message**. Add a message for the Dataflow job to pick up and pass through the model. For example, your input message could be "Tell the the sentiment of the following sentence: I like pineapple on pizza."

The Dataflow job outputs the response to the Pub/Sub sink topic. To check the response from the model, you can manually pull messages from the destination topic. For more information, see [Publish messages](https://cloud.google.com/pubsub/docs/publisher#publish-messages) in the Google Cloud documentation.

## Clean up resources

To avoid incurring charges to your Google Cloud account for the resources used in this example, clean up the resources that you created.


*   Cancel the streaming Dataflow job.
*   **Optional**: Archive the streaming Dataflow job.
*   Delete the Pub/Sub topic and subscriptions.
*   Delete the custom container from Artifact Registry.
*   Delete the created GCS bucket.
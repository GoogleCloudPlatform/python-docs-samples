# RunInference on Dataflow Streaming with Gemma

Gemma is a family of lightweight, state-of-the art open models built from research and technology used to create the Gemini models.
You can use Gemma models in your Apache Beam inference pipelines with the `RunInference` transform.

This example demonstrates how to use a Gemma model in a streaming Dataflow pipeline that has Pub/Sub sources and sinks.

For more information about using RunInference, see [Get started with AI/ML pipelines](https://beam.apache.org/documentation/ml/overview/) in the Apache Beam documentation.

## Before you begin

Follow the steps in this section to create the necessary environment to run this workflow.

### Enable Google Cloud services

This workflow uses multiple Google Cloud Platform products, including Dataflow, Pub/Sub, Google Cloud Storage, and Artifact Registry. Before you start the workflow, create a Google Cloud project that has the following services enabled:

* Dataflow
* Pub/Sub
* Google Cloud Storage
* Artifact Registry

Using these services incurs billing charges.

Your Google Cloud project also needs to have Nvidia L4 GPU quota. For more information, see [GPU quota](https://cloud.google.com/compute/resource-usage#gpu_quota) in the Google Cloud documentation.

### Create a custom container

To build a custom container, use Docker. This repository contains a Dockerfile that you can use to build your custom container. To build and push a container to Artifact Registry by using DockerFollow, follow the instructions in the [Build and push the image](https://cloud.google.com/dataflow/docs/guides/build-container-image#build_and_push_the_image) section of the "Build custom container images for Dataflow" page in the Google Cloud documentation.

### Create Pub/Sub topics for input and output

To create your Pub/Sub source and sink, follow the instructions in [Create a Pub/Sub topic](https://cloud.google.com/pubsub/docs/create-topic#pubsub_create_topic-Console) in the Google Cloud documentation. For this example, create two topics, one input topic and one output topic. For input, the topic must have a subscription that you can provide to the Gemma model. 

### Download and save the model

Save a version of the Gemma 2B model. Downloaded the model from [Kaggle](https://www.kaggle.com/models/keras/gemma/frameworks/keras/variations/gemma_2b_en). Rename the downloaded archive `gemma_2B`. This download is a directory, not a standalone file. 

### Optional: Create a new virtual environment

The Python major and minor version contained in the custom container must match the environment used for job submission. For this example, use Python version 3.11.

```
python3.11 -m venv /tmp/venv
source /tmp/venv/bin/activate
```

For more information, see [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html).

### Install dependencies

Install Apache Beam and the dependencies required to run the pipeline in your local environment. 

```
pip install -U -r requirements.txt
```

## Code Overview

This section provides details about the custom model handler and the formatting `DoFn` used in this example.

### Custom model handler

To simplify model loading, this notebook defines a custom model handler that loads the model by using the model's `from_preset` method. Using this method decreases the time needed to load Gemma.

To customize the behavior of the handler, implement the following methods: `load_model`, `validate_inference_args`, and `share_model_across_processes`.

The Keras implementation of the Gemma models has a `generate` method
that generates text based on a prompt. To route the prompts correctly, use this function in the `run_inference` function.

```py
class GemmaModelHandler(
    ModelHandler[str, PredictionResult, GemmaCausalLM]
):
    def __init__(
        self,
        model_name: str = "",
    ):
        """ Implementation of the ModelHandler interface for Gemma using text as input.

        Example Usage::

          pcoll | RunInference(GemmaModelHandler())

        Args:
          model_name: The Gemma model uri.
        """
        self._model_name = model_name
        self._env_vars = {}
    def share_model_across_processes(self)  -> bool:
        return True

    def load_model(self) -> GemmaCausalLM:
        """Loads and initializes a model for processing."""
        return keras_nlp.models.GemmaCausalLM.from_preset(self._model_name)

    def run_inference(
        self,
        batch: Sequence[str],
        model: GemmaCausalLM,
        inference_args: Optional[Dict[str, Any]] = None
    ) -> Iterable[PredictionResult]:
        """Runs inferences on a batch of text strings.

        Args:
          batch: A sequence of examples as text strings.
          model:
          inference_args: Any additional arguments for an inference.

        Returns:
          An Iterable of type PredictionResult.
        """
        # Loop each text string, and use a tuple to store the inference results.
        predictions = []
        for one_text in batch:
            result = model.generate(one_text, max_length=64)
            predictions.append(result)
        return [PredictionResult(x, y) for x, y in zip(batch, predictions)]
```

### Formatting DoFn

The output from a keyed model handler is a tuple of the form `(key, PredictionResult)`. To format that output into a string before sending it to the answer Pub/Sub topic, use an extra `DoFn`.

```py
class FormatOutput(beam.DoFn):
  def process(self, element, *args, **kwargs):
    yield "Key : {key}, Input: {input}, Output: {output}".format(key=element[0], input=element[1].example, output=element[1].inference)
```

## Start the pipeline
Run the following code from the directory to start the Dataflow streaming pipeline. Replace `$PROJECT`, `$GCS_BUCKET`, `$REGION`, `$CONTAINER_URI`, `$INPUT_TOPIC`, and `$OUTPUT_TOPIC` with the Google Cloud Project resources you created earlier. It may take around 5 minutes for the worker to start up and begin accepting messages from the input Pub/Sub topic. 

```
python custom_model_gemma.py \
  --runner=dataflowrunner \
  --project=$PROJECT \
  --temp_location=$GCS_BUCKET \
  --region=$REGION \
  --machine_type="g2-standard-4" \
  --sdk_container_image=$CONTAINER_URI \ 
  --disk_size_gb=200 \
  --dataflow_service_options="worker_accelerator=type:nvidia-l4;count:1;install-nvidia-driver:5xx" \
  --messages_subscription=$INPUT_SUBSCRIPTION \
  --responses_topic=$OUTPUT_TOPIC \
  --model_path="gemma_2B"
  --save_main_session
```

## Send a prompt to the model and check the response

In the Google Cloud console, navigate to the Pub/Sub topics page, and then select your input topic. On the **Messages** tab, click **Publish Message**. Add a message into the pipeline for the Dataflow job to pick up and pass through the model. The Dataflow job outputs the response to the Pub/Sub sink topic. To check the response from the model, you can manually pull messages from the destination topic. For more information, see [Publish messages](https://cloud.google.com/pubsub/docs/publisher#publish-messages) in the Google Cloud documentation.

## Clean up resources

To avoid incurring charges to your Google Cloud account for the resources used in this example, clean up the resources that you created.


*   Cancel the streaming Dataflow job.
*   Delete the Pub/Sub topic and subscriptions.
*   Delete the custom container from Artifact Registry.
*   Empty the `tmp` directory of your Google Cloud Storage bucket.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import keras_nlp
import logging

import apache_beam as beam
from apache_beam.ml.inference.base import RunInference
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import WorkerOptions
from apache_beam.ml.inference.base import ModelHandler
from apache_beam.ml.inference.base import PredictionResult
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Sequence

model_path = "gemma_2B"
topic_question="projects/google.com:clouddfe/subscriptions/gemma-input-a"
topic_answer="projects/google.com:clouddfe/topics/jrmccluskey"

# Define `SpacyModelHandler` to load the model and perform the inference.

from apache_beam.ml.inference.base import ModelHandler
from apache_beam.ml.inference.base import PredictionResult
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Sequence
from keras_nlp.src.models.gemma.gemma_causal_lm import GemmaCausalLM

class GemmaModelHandler(ModelHandler[str,
                                     PredictionResult,GemmaCausalLM
                                     ]):
    def __init__(
        self,
        model_name: str = "gemma_2B",
    ):
        """ Implementation of the ModelHandler interface for spaCy using text as input.

        Example Usage::

          pcoll | RunInference(SpacyModelHandler())

        Args:
          model_name: The Gemma model name. Default is gemma_2B.
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

class FormatOutput(beam.DoFn):
  def process(self, element, *args, **kwargs):
    yield "Input: {input}, Output: {output}".format(input=element.example, output=element.inference)

# Specify the model handler, providing a path and the custom inference function.
options = PipelineOptions()
options.view_as(StandardOptions).streaming = True
options.view_as(SetupOptions).save_main_session = True


options.view_as(StandardOptions).runner = "dataflowrunner"
options.view_as(GoogleCloudOptions).project = "google.com:clouddfe"
options.view_as(GoogleCloudOptions).temp_location= "gs://clouddfe-jrmccluskey/tmp"
options.view_as(GoogleCloudOptions).region= "us-central1"
options.view_as(WorkerOptions).machine_type= "g2-standard-4"
options.view_as(WorkerOptions).worker_harness_container_image = "us-central1-docker.pkg.dev/google.com/clouddfe/jrmccluskey-images/dataflow/gemma-dataflow:d4"
options.view_as(WorkerOptions).disk_size_gb=200
options.view_as(GoogleCloudOptions).dataflow_service_options=["worker_accelerator=type:nvidia-l4;count:1;install-nvidia-driver"]

def run():
  with beam.Pipeline(options=options) as p:
    _ = (p | "Read Topic A" >> beam.io.ReadFromPubSub(subscription=topic_question)
           | "Parse" >> beam.Map(lambda x: x.decode("utf-8"))
           | "RunInference-Gemma" >> RunInference(GemmaModelHandler(model_path)) # Send the prompts to the model and get responses.
           | "Format Output" >> beam.ParDo(FormatOutput()) # Format the output.
           | "Publish Result" >> beam.io.gcp.pubsub.WriteStringsToPubSub(topic=topic_answer)
  )

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--messages_topic",
    required=True,
    help="Pub/Sub topic for input text messages",
  )
  parser.add_argument(
    "--responses_topic",
    required=True,
    help="Pub/Sub topic for output text responses",
  )
  parser.add_argument(
    "--model_path",
    required=False,
    default="gemma_2B",
    help="path to the Gemma model in the custom worker contaienr",
  )

  args, beam_args = parser.parse_known_args()

  logging.getLogger().setLevel(logging.INFO)
  beam_options = PipelineOptions(
        beam_args,
        pickle_library="cloudpickle",
        streaming=True,
  )

  with beam.Pipeline(options=beam_options) as p:
    _ = (p | "Read Topic" >> beam.io.ReadFromPubSub(subscription=args.messages_topic)
           | "Parse" >> beam.Map(lambda x: x.decode("utf-8"))
           | "RunInference-Gemma" >> RunInference(GemmaModelHandler(args.model_path)) # Send the prompts to the model and get responses.
           | "Format Output" >> beam.ParDo(FormatOutput()) # Format the output.
           | "Publish Result" >> beam.io.gcp.pubsub.WriteStringsToPubSub(topic=args.responeses_topic)
  )
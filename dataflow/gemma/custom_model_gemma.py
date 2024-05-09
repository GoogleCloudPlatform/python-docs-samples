# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Iterable, Sequence

import logging

from typing import Any
from typing import Optional

import apache_beam as beam
from apache_beam.ml.inference import utils
from apache_beam.ml.inference.base import ModelHandler
from apache_beam.ml.inference.base import PredictionResult
from apache_beam.ml.inference.base import RunInference
from apache_beam.options.pipeline_options import PipelineOptions

import keras_nlp
from keras_nlp.src.models.gemma.gemma_causal_lm import GemmaCausalLM


class GemmaModelHandler(ModelHandler[str, PredictionResult, GemmaCausalLM]):
    def __init__(
        self,
        model_name: str = "gemma_2B",
    ):
        """ Implementation of the ModelHandler interface for Gemma using text as input.

        Example Usage::

          pcoll | RunInference(GemmaModelHandler())

        Args:
          model_name: The Gemma model name. Default is gemma_2B.
        """
        self._model_name = model_name
        self._env_vars = {}

    def share_model_across_processes(self) -> bool:
        """ Indicates if the model should be loaded once-per-VM rather than
        once-per-worker-process on a VM. Because Gemma is a large language model,
        this will always return True to avoid OOM errors.
        """
        return True

    def load_model(self) -> GemmaCausalLM:
        """Loads and initializes a model for processing."""
        return keras_nlp.models.GemmaCausalLM.from_preset(self._model_name)

    def run_inference(
        self,
        batch: Sequence[str],
        model: GemmaCausalLM,
        inference_args: Optional[dict[str, Any]] = None
    ) -> Iterable[PredictionResult]:
        """Runs inferences on a batch of text strings.

        Args:
          batch: A sequence of examples as text strings.
          model: The Gemma model being used.
          inference_args: Any additional arguments for an inference.

        Returns:
          An Iterable of type PredictionResult.
        """
        # Loop each text string, and use a tuple to store the inference results.
        predictions = []
        for one_text in batch:
            result = model.generate(one_text, max_length=64)
            predictions.append(result)
        return utils._convert_to_result(batch, predictions, self._model_name)


class FormatOutput(beam.DoFn):
    def process(self, element, *args, **kwargs):
        yield "Input: {input}, Output: {output}".format(
            input=element.example, output=element.inference)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--messages_subscription",
        required=True,
        help="Pub/Sub subscription for input text messages",
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
        help="path to the Gemma model in the custom worker container",
    )

    args, beam_args = parser.parse_known_args()

    logging.getLogger().setLevel(logging.INFO)
    beam_options = PipelineOptions(
        beam_args,
        streaming=True,
    )

    pipeline = beam.Pipeline(options=beam_options)
    _ = (
        pipeline | "Read Topic" >>
        beam.io.ReadFromPubSub(subscription=args.messages_subscription)
        | "Parse" >> beam.Map(lambda x: x.decode("utf-8"))
        | "RunInference-Gemma" >> RunInference(
            GemmaModelHandler(args.model_path)
        )  # Send the prompts to the model and get responses.
        | "Format Output" >> beam.ParDo(FormatOutput())  # Format the output.
        | "Publish Result" >>
        beam.io.gcp.pubsub.WriteStringsToPubSub(topic=args.responses_topic))
    pipeline.run()

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
import json
import logging

import apache_beam as beam
from apache_beam.ml.inference.base import ModelHandler
from apache_beam.ml.inference.base import PredictionResult
from apache_beam.ml.inference.base import RunInference
from apache_beam.options.pipeline_options import PipelineOptions

from gemma.config import get_config_for_2b
from gemma.config import get_config_for_7b
from gemma.model import GemmaForCausalLM

import torch


class GemmaPytorchModelHandler(ModelHandler[str, PredictionResult, GemmaForCausalLM]):
    def __init__(
        self,
        model_variant: str,
        checkpoint_path: str,
        tokenizer_path: str,
        device: str | None = "cpu",
    ):
        """Implementation of the ModelHandler interface for Gemma-on-Pytorch
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
        model_config = (
            get_config_for_2b() if "2b" in model_variant else get_config_for_7b()
        )
        model_config.tokenizer = tokenizer_path
        model_config.quant = "quant" in model_variant
        model_config.tokenizer = tokenizer_path

        self._model_config = model_config
        self._checkpoint_path = checkpoint_path
        if device == "GPU":
            logging.info("Device is set to CUDA")
            self._device = torch.device("cuda")
        else:
            logging.info("Device is set to CPU")
            self._device = torch.device("cpu")
        self._env_vars = {}

    def share_model_across_processes(self) -> bool:
        """Allows us to load a model only once per worker VM, decreasing
        pipeline memory requirements.
        """
        return True

    def load_model(self) -> GemmaForCausalLM:
        """Loads and initializes a model for processing."""
        torch.set_default_dtype(self._model_config.get_dtype())
        model = GemmaForCausalLM(self._model_config)
        model.load_weights(self._checkpoint_path)
        model = model.to(self._device).eval()
        return model

    def run_inference(
        self,
        batch: Sequence[str],
        model: GemmaForCausalLM,
        inference_args: dict | None = None,
    ) -> Iterable[PredictionResult]:
        """Runs inferences on a batch of text strings.

        Args:
          batch: A sequence of examples as text strings.
          model: The Gemma model being used.
          inference_args: Any additional arguments for an inference.

        Returns:
          An Iterable of type PredictionResult.
        """
        result = model.generate(prompts=batch, device=self._device)
        predictions = [result]
        return [PredictionResult(x, y) for x, y in zip(batch, predictions)]


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
        "--model_variant",
        required=False,
        default="gemma-2b-it",
        help="name of the gemma variant being used",
    )
    parser.add_argument(
        "--checkpoint_path",
        required=False,
        default="pytorch_model/gemma-2b-it.ckpt",
        help="path to the Gemma model weights in the custom worker container",
    )
    parser.add_argument(
        "--tokenizer_path",
        required=False,
        default="pytorch_model/tokenizer.model",
        help="path to the Gemma tokenizer in the custom worker container",
    )
    parser.add_argument(
        "--device",
        required=False,
        default="cpu",
        help="device to run the model on",
    )

    args, beam_args = parser.parse_known_args()

    config = get_config_for_2b()

    logging.getLogger().setLevel(logging.INFO)
    beam_options = PipelineOptions(
        beam_args,
        save_main_session=True,
        streaming=True,
    )

    handler = GemmaPytorchModelHandler(
        model_variant=args.model_variant,
        checkpoint_path=args.checkpoint_path,
        tokenizer_path=args.tokenizer_path,
        device=args.device,
    )

    with beam.Pipeline(options=beam_options) as pipeline:
        _ = (
            pipeline
            | "Subscribe to Pub/Sub" >> beam.io.ReadFromPubSub(subscription=args.messages_subscription)
            | "Decode" >> beam.Map(lambda msg: msg.decode("utf-8"))
            | "RunInference Gemma" >> RunInference(handler)
            | "Format output" >> beam.Map(
                lambda response: json.dumps(
                    {"input": response.example, "outputs": response.inference}
                )
            )
            | "Encode" >> beam.Map(lambda msg: msg.encode("utf-8"))
            | "Publish to Pub/Sub" >> beam.io.gcp.pubsub.WriteToPubSub(topic=args.responses_topic)
        )

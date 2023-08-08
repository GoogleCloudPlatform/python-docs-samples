# Copyright 2023 Google LLC
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

"""Runs a streaming RunInference Language Model pipeline."""

from __future__ import annotations

import logging

import apache_beam as beam
from apache_beam.ml.inference.base import PredictionResult
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.pytorch_inference import make_tensor_model_fn
from apache_beam.ml.inference.pytorch_inference import PytorchModelHandlerTensor
from apache_beam.options.pipeline_options import PipelineOptions
import torch
from transformers import AutoConfig
from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer

MAX_RESPONSE_TOKENS = 256


def to_tensors(input_text: str, tokenizer: PreTrainedTokenizer) -> torch.Tensor:
    """Encodes input text into token tensors.

    Args:
        input_text: Input text for the language model.
        tokenizer: Tokenizer for the language model.

    Returns: Tokenized input tokens.
    """
    return tokenizer(input_text, return_tensors="pt").input_ids[0]


def decode_response(result: PredictionResult, tokenizer: PreTrainedTokenizer) -> str:
    """Decodes output token tensors into text.

    Args:
        result: Prediction results from the RunInference transform.
        tokenizer: Tokenizer for the language model.

    Returns: The model's response as text.
    """
    output_tokens = result.inference
    return tokenizer.decode(output_tokens, skip_special_tokens=True)


class AskModel(beam.PTransform):
    """Asks an language model a prompt message and gets its responses.

    Attributes:
        model_name: HuggingFace model name compatible with AutoModelForSeq2SeqLM.
        state_dict_path: File path to the model's state_dict, can be in Cloud Storage.
        max_response_tokens: Maximum number of tokens for the model to generate.
    """

    def __init__(
        self,
        model_name: str,
        state_dict_path: str,
        max_response_tokens: int = MAX_RESPONSE_TOKENS,
    ) -> None:
        self.model_handler = PytorchModelHandlerTensor(
            state_dict_path=state_dict_path,
            model_class=AutoModelForSeq2SeqLM.from_config,
            model_params={"config": AutoConfig.from_pretrained(model_name)},
            inference_fn=make_tensor_model_fn("generate"),
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_response_tokens = max_response_tokens

    def expand(self, pcollection: beam.PCollection[str]) -> beam.PCollection[str]:
        return (
            pcollection
            | "To tensors" >> beam.Map(to_tensors, self.tokenizer)
            | "RunInference"
            >> RunInference(
                self.model_handler,
                inference_args={"max_new_tokens": self.max_response_tokens},
            )
            | "Get response" >> beam.Map(decode_response, self.tokenizer)
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--messages-topic",
        required=True,
        help="Pub/Sub topic for input text messages",
    )
    parser.add_argument(
        "--responses-topic",
        required=True,
        help="Pub/Sub topic for output text responses",
    )
    parser.add_argument(
        "--model-name",
        required=True,
        help="HuggingFace model name compatible with AutoModelForSeq2SeqLM",
    )
    parser.add_argument(
        "--state-dict-path",
        required=True,
        help="File path to the model's state_dict, can be in Cloud Storage",
    )
    args, beam_args = parser.parse_known_args()

    logging.getLogger().setLevel(logging.INFO)
    beam_options = PipelineOptions(
        beam_args,
        pickle_library="cloudpickle",
        streaming=True,
    )

    simple_name = args.model_name.split("/")[-1]
    pipeline = beam.Pipeline(options=beam_options)
    _ = (
        pipeline
        | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(args.messages_topic)
        | "Decode bytes" >> beam.Map(lambda msg: msg.decode("utf-8"))
        | f"Ask {simple_name}" >> AskModel(args.model_name, args.state_dict_path)
        | "Encode bytes" >> beam.Map(lambda msg: msg.encode("utf-8"))
        | "Write to Pub/Sub" >> beam.io.WriteToPubSub(args.responses_topic)
    )
    pipeline.run()

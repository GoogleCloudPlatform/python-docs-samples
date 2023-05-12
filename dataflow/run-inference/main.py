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

"""Runs a streaming RunInference LLM pipeline."""

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

MAX_RESPONSE_TOKENS = 256


class RunPipeline(beam.PTransform):
    def __init__(self, model_name: str, state_dict_path: str) -> None:
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model_handler = PytorchModelHandlerTensor(
            state_dict_path=state_dict_path,
            model_class=AutoModelForSeq2SeqLM.from_config,
            model_params={"config": AutoConfig.from_pretrained(model_name)},
            inference_fn=make_tensor_model_fn("generate"),
        )

    def expand(self, pcoll: beam.PCollection[str]) -> beam.PCollection[str]:
        return (
            pcoll
            | "Encode tokens" >> beam.Map(encode_inputs, self.tokenizer)
            | "RunInference"
            >> RunInference(
                self.model_handler,
                inference_args={"max_new_tokens": MAX_RESPONSE_TOKENS},
            )
            | "Decode tokens" >> beam.Map(decode_outputs, self.tokenizer)
        )


def encode_inputs(input_text: str, tokenizer: AutoTokenizer) -> torch.Tensor:
    """Encodes input text into token tensors.

    Args:
        input_text: Input text for the LLM model.
        tokenizer: Tokenizer for the LLM model.

    Returns: Tokenized input tokens.
    """
    return tokenizer(input_text, return_tensors="pt").input_ids[0]


def decode_outputs(result: PredictionResult, tokenizer: AutoTokenizer) -> str:
    """Decodes output token tensors into text.

    Args:
        result: Prediction results from the RunInference transform.
        tokenizer: Tokenizer for the LLM model.

    Returns: The model's response as text.
    """
    output_tokens = result.inference
    return tokenizer.decode(output_tokens, skip_special_tokens=True)


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
        save_main_session=True,
        streaming=True,
        requirements_file="requirements.txt",
    )
    with beam.Pipeline(options=beam_options) as pipeline:
        _ = (
            pipeline
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(args.messages_topic)
            | "Decode bytes" >> beam.Map(lambda msg: msg.decode("utf-8"))
            | "Run pipeline" >> RunPipeline(args.model_name, args.state_dict_path)
            | "Write to Pub/Sub" >> beam.io.WriteToPubSub(args.responses_topic)
        )

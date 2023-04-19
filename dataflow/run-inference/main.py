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

from __future__ import annotations

import logging

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.pytorch_inference import PytorchModelHandlerTensor
from apache_beam.ml.inference.pytorch_inference import make_tensor_model_fn
from apache_beam.options.pipeline_options import PipelineOptions
from transformers import AutoConfig
from transformers import AutoTokenizer
from transformers import T5ForConditionalGeneration

DEFAULT_MODEL = "google/flan-t5-small"
DEFAULT_PROMPT = "translate English to German"


def encode_tokens(input_text: str, tokenizer: AutoTokenizer):
    return tokenizer(input_text, return_tensors="pt").input_ids[0]


def decode_tokens(output_tokens, tokenizer: AutoTokenizer):
    return tokenizer.decode(output_tokens.inference, skip_special_tokens=True)


def run(
    cache_path: str,
    model_name: str = DEFAULT_MODEL,
    prompt: str = DEFAULT_PROMPT,
    beam_options: PipelineOptions | None = None,
) -> None:
    model_handler = PytorchModelHandlerTensor(
        state_dict_path=FileSystems.join(cache_path, model_name, "state_dict.pt"),
        model_class=T5ForConditionalGeneration,
        model_params={"config": AutoConfig.from_pretrained(model_name)},
        inference_fn=make_tensor_model_fn("generate"),
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    with beam.Pipeline(options=beam_options) as pipeline:
        _ = (
            pipeline
            | beam.Create(["The house is wonderful.", "We love trees!"])
            | "Make prompt" >> beam.Map(lambda request: f"{prompt}: {request}")
            | "Encode tokens" >> beam.Map(encode_tokens, tokenizer)
            | "RunInference"
            >> RunInference(model_handler, inference_args={"max_new_tokens": 256})
            | "Decode tokens" >> beam.Map(decode_tokens, tokenizer)
            | beam.Map(lambda x: print(x))
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-cache-path", required=True)
    parser.add_argument("--model-name", default=DEFAULT_MODEL)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    args, beam_args = parser.parse_known_args()

    logging.getLogger().setLevel(logging.INFO)
    beam_options = PipelineOptions(
        beam_args,
        save_main_session=True,
        requirements_file="requirements.txt",
    )
    run(
        cache_path=args.model_cache_path,
        model_name=args.model_name,
        prompt=args.prompt,
        beam_options=beam_options,
    )

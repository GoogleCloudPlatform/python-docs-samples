# Copyright 2021 Google LLC
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

import argparse
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import tensorflow as tf


def check_gpus(_: None, gpus_optional: bool = False) -> None:
    """Validates that we are detecting GPUs, otherwise raise a RuntimeError."""
    gpu_devices = tf.config.list_physical_devices("GPU")
    if gpu_devices:
        logging.info(f"Using GPU: {gpu_devices}")
    elif gpus_optional:
        logging.warning("No GPUs found, defaulting to CPU.")
    else:
        raise RuntimeError("No GPUs found.")


def run(input_text: str, beam_args: list[str] | None = None) -> None:
    beam_options = PipelineOptions(beam_args, save_main_session=True)
    pipeline = beam.Pipeline(options=beam_options)
    (
        pipeline
        | "Create data" >> beam.Create([input_text])
        | "Check GPU availability"
        >> beam.Map(
            lambda x, unused_side_input: x,
            unused_side_input=beam.pvalue.AsSingleton(
                pipeline | beam.Create([None]) | beam.Map(check_gpus)
            ),
        )
        | "My transform" >> beam.Map(logging.info)
    )
    pipeline.run()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-text",
        default="Hello!",
        help="Input text to display.",
    )
    args, beam_args = parser.parse_known_args()

    run(args.input_text, beam_args)

# Copyright 2024 Google LLC
#
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

"""Defines a pipeline to create a banner from the longest word in the input."""

import apache_beam as beam

from my_package import my_transforms
from my_package.utils import figlet


def longest_word_pipeline(
    input_path: str, output_path: str, pipeline_options_args: list[str]
) -> beam.Pipeline:
    """Instantiates and returns a Beam pipeline object"""

    pipeline_options = beam.options.pipeline_options.PipelineOptions(
        pipeline_options_args
    )

    pipeline = beam.Pipeline(options=pipeline_options)
    _ = (
        pipeline
        | "Read Input" >> beam.io.ReadFromText(input_path)
        | "Find the Longest Word" >> my_transforms.FindLongestWord()
        | "Create a Banner" >> beam.Map(figlet.render)
        | "Write Output" >> beam.io.WriteToText(output_path)
    )

    return pipeline

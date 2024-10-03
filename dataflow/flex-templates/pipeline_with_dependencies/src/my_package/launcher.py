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

"""Defines command line arguments for the pipeline defined in the package."""

import argparse

from my_package import my_pipeline


def run(argv: list[str] | None = None):
    """Parses the parameters provided on the command line and runs the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file(s) to process")
    parser.add_argument("--output", required=True, help="Output file")

    pipeline_args, other_args = parser.parse_known_args(argv)

    pipeline = my_pipeline.longest_word_pipeline(
        pipeline_args.input, pipeline_args.output, other_args
    )

    pipeline.run()

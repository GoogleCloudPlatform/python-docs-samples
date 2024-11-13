#!/usr/bin/env python
#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import apache_beam as beam
from apache_beam.io.textio import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions


def write_to_cloud_storage(argv=None):
    # Parse the pipeline options passed into the application.
    class MyOptions(PipelineOptions):
        @classmethod
        # Define a custom pipeline option that specfies the Cloud Storage bucket.
        def _add_argparse_args(cls, parser):
            parser.add_argument("--output", required=True)

    wordsList = ["1", "2", "3", "4"]
    options = MyOptions()

    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | "Create elements" >> beam.Create(wordsList)
            | "Write Files" >> WriteToText(options.output, file_name_suffix=".txt")
        )


if __name__ == "__main__":
    write_to_cloud_storage()

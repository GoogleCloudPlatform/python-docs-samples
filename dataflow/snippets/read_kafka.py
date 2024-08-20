#!/usr/bin/env python
#  Copyright 2024 Google LLC
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

# [START dataflow_kafka_read]
import argparse

import apache_beam as beam

from apache_beam import window
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.io.textio import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions


def read_from_kafka() -> None:

    # Parse the pipeline options passed into the application. Example:
    #     --topic=$KAFKA_TOPIC --bootstrap_server=$BOOTSTRAP_SERVER
    #     --output=$CLOUD_STORAGE_BUCKET --streaming
    # For more information, see
    # https://beam.apache.org/documentation/programming-guide/#configuring-pipeline-options
    class MyOptions(PipelineOptions):
        @staticmethod
        def _add_argparse_args(parser: argparse.ArgumentParser) -> None:
            parser.add_argument('--topic')
            parser.add_argument('--bootstrap_server')
            parser.add_argument('--output')

    options = MyOptions()
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            # Read messages from an Apache Kafka topic.
            | ReadFromKafka(
                consumer_config={
                    "bootstrap.servers": options.bootstrap_server
                },
                topics=[options.topic],
                with_metadata=False,
                max_num_records=5,
                start_read_time=0
            )
            # The previous step creates a key-value collection, keyed by message ID.
            # The values are the message payloads.
            | beam.Values()
            # Subdivide the output into fixed 5-second windows.
            | beam.WindowInto(window.FixedWindows(5))
            | WriteToText(
                file_path_prefix=options.output,
                file_name_suffix='.txt',
                num_shards=1)
        )
# [END dataflow_kafka_read]


if __name__ == "__main__":
    read_from_kafka()

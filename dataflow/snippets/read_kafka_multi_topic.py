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

# [START dataflow_kafka_read_multi_topic]
import argparse

import apache_beam as beam

from apache_beam.io.kafka import ReadFromKafka
from apache_beam.io.textio import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions


def read_from_kafka() -> None:
    # Parse the pipeline options passed into the application. Example:
    #   --bootstrap_server=$BOOTSTRAP_SERVER --output=$STORAGE_BUCKET --streaming
    # For more information, see
    # https://beam.apache.org/documentation/programming-guide/#configuring-pipeline-options
    class MyOptions(PipelineOptions):
        @staticmethod
        def _add_argparse_args(parser: argparse.ArgumentParser) -> None:
            parser.add_argument('--bootstrap_server')
            parser.add_argument('--output')

    options = MyOptions()
    with beam.Pipeline(options=options) as pipeline:
        # Read from two Kafka topics.
        all_topics = pipeline | ReadFromKafka(consumer_config={
                "bootstrap.servers": options.bootstrap_server
            },
            topics=["topic1", "topic2"],
            with_metadata=True,
            max_num_records=10,
            start_read_time=0
        )

        # Filter messages from one topic into one branch of the pipeline.
        (all_topics
            | beam.Filter(lambda message: message.topic == 'topic1')
            | beam.Map(lambda message: message.value.decode('utf-8'))
            | "Write topic1" >> WriteToText(
                file_path_prefix=options.output + '/topic1/output',
                file_name_suffix='.txt',
                num_shards=1))

        # Filter messages from the other topic.
        (all_topics
            | beam.Filter(lambda message: message.topic == 'topic2')
            | beam.Map(lambda message: message.value.decode('utf-8'))
            | "Write topic2" >> WriteToText(
                file_path_prefix=options.output + '/topic2/output',
                file_name_suffix='.txt',
                num_shards=1))
# [END dataflow_kafka_read_multi_topic]


if __name__ == "__main__":
    read_from_kafka()

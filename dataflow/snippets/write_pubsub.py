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

# [START dataflow_pubsub_write_with_attributes]
import argparse
from typing import Any, Dict, List

import apache_beam as beam
from apache_beam.io import PubsubMessage
from apache_beam.io import WriteToPubSub
from apache_beam.options.pipeline_options import PipelineOptions

from typing_extensions import Self


def item_to_message(item: Dict[str, Any]) -> PubsubMessage:
    # Re-import needed types. When using the Dataflow runner, this
    # function executes on a worker, where the global namespace is not
    # available. For more information, see:
    # https://cloud.google.com/dataflow/docs/guides/common-errors#name-error
    from apache_beam.io import PubsubMessage

    attributes = {"buyer": item["name"], "timestamp": str(item["ts"])}
    data = bytes(item["product"], "utf-8")

    return PubsubMessage(data=data, attributes=attributes)


def write_to_pubsub(argv: List[str] = None) -> None:
    # Parse the pipeline options passed into the application. Example:
    #     --topic=$TOPIC_PATH --streaming
    # For more information, see
    # https://beam.apache.org/documentation/programming-guide/#configuring-pipeline-options
    class MyOptions(PipelineOptions):
        @classmethod
        # Define a custom pipeline option to specify the Pub/Sub topic.
        def _add_argparse_args(cls: Self, parser: argparse.ArgumentParser) -> None:
            parser.add_argument("--topic", required=True)

    example_data = [
        {"name": "Robert", "product": "TV", "ts": 1613141590000},
        {"name": "Maria", "product": "Phone", "ts": 1612718280000},
        {"name": "Juan", "product": "Laptop", "ts": 1611618000000},
        {"name": "Rebeca", "product": "Video game", "ts": 1610000000000},
    ]
    options = MyOptions()

    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | "Create elements" >> beam.Create(example_data)
            | "Convert to Pub/Sub messages" >> beam.Map(item_to_message)
            | WriteToPubSub(topic=options.topic, with_attributes=True)
        )

    print("Pipeline ran successfully.")


# [END dataflow_pubsub_write_with_attributes]


if __name__ == "__main__":
    write_to_pubsub()

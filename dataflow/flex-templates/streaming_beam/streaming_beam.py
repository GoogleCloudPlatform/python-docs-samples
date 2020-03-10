#!/usr/bin/env python
#
# Copyright 2020 Google Inc. All Rights Reserved.
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

"""An Apache Beam streaming pipeline example.

It reads JSON encoded messages from Pub/Sub, transforms the message data and
writes the results to BigQuery.
"""

from __future__ import absolute_import

import argparse
import json
import logging
import time

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.window as window

# Defines the BigQuery schema for the output table.
SCHEMA = ','.join([
    'url:STRING',
    'num_reviews:INTEGER',
    'score:FLOAT64',
    'first_date:TIMESTAMP',
    'last_date:TIMESTAMP',
])


def run(args, input_subscription, output_table):
  """Build and run the pipeline."""
  options = PipelineOptions(args, save_main_session=True, streaming=True)

  with beam.Pipeline(options=options) as pipeline:

    # Read from PubSub into a PCollection.
    messages = (
        pipeline
        | 'Read form Pub/Sub' >> beam.io.ReadFromPubSub(
            subscription=input_subscription).with_output_types(bytes)
        | 'UTF-8 bytes to string' >> beam.Map(lambda msg: msg.decode('utf-8')))

    # Parse the input json message and add 'score' & 'processing_time' keys.
    def parse_json_message(message):
      row = json.loads(message)
      return {
          'url': row['url'],
          'score': 1.0 if row['review'] == 'positive' else 0.0,
          'processing_time': int(time.time()),
      }

    # Count the occurrences of each url, average score and the corresponding
    # min/max timestamps.
    def get_statistics(url_messages):
      url, messages = url_messages
      return {
          'url': url,
          'num_reviews': len(messages),
          'score': sum(msg['score'] for msg in messages) / len(messages),
          'first_date': min(msg['processing_time'] for msg in messages),
          'last_date': max(msg['processing_time'] for msg in messages),
      }

    url_values = (
        messages
        | 'Parse JSON messages' >> beam.Map(parse_json_message)
        | 'Fixed-size windows' >> beam.WindowInto(window.FixedWindows(
            60, 0))  # 1 minute
        | 'Add URL keys' >> beam.Map(lambda msg: (msg['url'], msg))
        | 'Group by URLs' >> beam.GroupByKey()
        | 'Get statistics' >> beam.Map(get_statistics))

    # Output the results into BigQuery table.
    _ = url_values | 'Write' >> beam.io.WriteToBigQuery(
        output_table, schema=SCHEMA)

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--output_table',
      help=(
          'Output BigQuery table for results specified as: '
          'PROJECT:DATASET.TABLE or DATASET.TABLE.'))
  parser.add_argument(
      '--input_subscription',
      help=(
          'Input PubSub subscription of the form '
          '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
  known_args, pipeline_args = parser.parse_known_args()
  run(pipeline_args, known_args.input_subscription, known_args.output_table)


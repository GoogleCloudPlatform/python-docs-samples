#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.py
#

"""An Apache Beam streaming pipeline that reads JSON encoded messages from Pub/Sub, transform the message data and writes the results to BigQuery.
"""

from __future__ import absolute_import

import argparse
import logging
import json

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
import apache_beam.transforms.window as window


# Defines the BigQuery schema for the output table.
SCHEMA = ('url:STRING,'
          'num_reviews:INTEGER,'
          'score:FLOAT64,'
          'first_date:TIMESTAMP,'
          'last_date:TIMESTAMP')


class ParseJsonMessageDoFn(beam.DoFn):
  """Parse the json encoded text message into a dict."""

  def __init__(self):
    beam.DoFn.__init__(self)

  def process(self, element):
    """Returns an iterator over the tuple: (message's url, dict).

    Args:
      element: the element json message to be processed.
    Returns:
      The tuple of url string and the dict.
      The dict contain the keys: 'url', 'review', 'score' and 'processing_time'.
    """
    import time
    row = json.loads(element)
    row['score'] = 0.0
    if row['review'] == 'positive':
      row['score'] = 1.0
    row['processing_time'] = int(time.time())
    return [(row['url'], row)]


def run(argv=None):
  """Build and run the pipeline."""
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--output_table',
      help=(
          'Output BigQuery table for results specified as: '
          'PROJECT:DATASET.TABLE or DATASET.TABLE.'))

  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument(
      '--input_topic',
      help=(
          'Input PubSub topic of the form '
          '"projects/<PROJECT>/topics/<TOPIC>".'))
  group.add_argument(
      '--input_subscription',
      help=(
          'Input PubSub subscription of the form '
          '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
  known_args, pipeline_args = parser.parse_known_args(argv)

  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(StandardOptions).streaming = True
  with beam.Pipeline(options=pipeline_options) as p:

    # Read from PubSub into a PCollection.
    if known_args.input_subscription:
      messages = (
          p
          | beam.io.ReadFromPubSub(subscription=known_args.input_subscription).
          with_output_types(bytes))
    else:
      messages = (
          p
          | beam.io.ReadFromPubSub(
              topic=known_args.input_topic).with_output_types(bytes))

    lines = messages | 'decode' >> beam.Map(lambda x: x.decode('utf-8'))

    # Count the occurrences of each url, average score and the corresponding
    # min/max timestamps.
    def aggregate_values(url_dict):
      (url, dict_list) = url_dict
      num_reviews = len(dict_list)
      avg_score = sum(i['score'] for i in dict_list) / len(dict_list)
      min_timestamp = min(i['processing_time'] for i in dict_list)
      max_timestamp = max(i['processing_time'] for i in dict_list)
      return (url, num_reviews, avg_score, min_timestamp, max_timestamp)

    url_values = (
        lines
        | 'split' >> (beam.ParDo(ParseJsonMessageDoFn()))
        | beam.WindowInto(window.FixedWindows(60, 0))
        | 'group' >> beam.GroupByKey()
        | 'aggregate' >> beam.Map(aggregate_values))

    # Format the tuples into a PCollection of dicts.
    def format_result(url_row):
      (url, num_reviews, avg_score, first_date, last_date) = url_row
      return {
          'url': url,
          'num_reviews': num_reviews,
          'score': avg_score,
          'first_date': first_date,
          'last_date': last_date
      }

    output = (
        url_values
        | 'format' >> beam.Map(format_result))

    # Output the results into BigQuery table.
    _ = output | 'Write' >> beam.io.WriteToBigQuery(
        known_args.output_table, schema=SCHEMA)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()


# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import json
import logging
from typing import List

from apache_beam import CombineFn, CombineGlobally, DoFn, io, ParDo, Pipeline, WindowInto
from apache_beam.error import PipelineError
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.window import FixedWindows

from google.cloud import dlp_v2, logging_v2


# For more details about info types format, please see
# https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig
INSPECT_CFG = {
  'info_types': [
    {'name': 'US_SOCIAL_SECURITY_NUMBER'}
  ]
}

# For more details about transformation format, please see
# https://cloud.google.com/dlp/docs/reference/rest/v2/projects.deidentifyTemplates#DeidentifyTemplate.InfoTypeTransformations
REDACTION_CFG = {
  'info_type_transformations': {
    'transformations': [
      {
        'primitive_transformation': {
          'character_mask_config': {
            'masking_character': '#'
          }
        }
      }
]}}   


class PayloadAsJson(DoFn):
  '''Convert PubSub message payload to UTF-8 and return as Json'''
  def process(self, element):
    yield json.loads(element.decode('utf-8'))


class BatchPayloads(CombineFn):
  '''Opinionated way to batch all payloads in the window'''

  def create_accumulator(self):
    return []

  def add_input(self, accumulator, input):
    accumulator.append(input)
    return accumulator

  def merge_accumulators(self, accumulators):
    merged = []
    for accumulator in accumulators:
      for item in accumulator:
        merged.append(item)
    return merged

  def extract_output(self, accumulator):
    return accumulator


class LogRedaction(beam.DoFn):
  '''Apply inspection and redaction to textPayload field of log entries'''

  def __init__(self, project_id: str):
    self.project_id = project_id
    self.dlp_client = None

  def _log_to_row(self, entry):
    # Make `Row` from `textPayload`. For more details on the row, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Row
    payload = entry['textPayload'] if entry.get('textPayload') else ''
    return {'values': [{'string_value': payload}]}

  def setup(self):
    '''Initialize DLP client'''
    if self.dlp_client:
      return
    self.dlp_client = dlp_v2.DlpServiceClient(client_options={'quota_project_id', self.project_id})
    if not self.dlp_client:
      logging.error('Cannot create Google DLP Client')
      raise PipelineError('Cannot create Google DLP Client')

  def process(self, logs):
    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    table = {
      'table': {
        'headers': {'name': 'textPayload'},
        'rows': map(self._log_to_row, logs)
    }}

    response = self.dlp_client.deidentify_content(
      request={
        'parent': f'projects/{self.project_id}',
        'inspect_config': INSPECT_CFG,
        'deidentify_config': REDACTION_CFG,
        'item': table_item,
      })

    # replace payload with redacted version
    modified_logs = []
    for i in range(len(logs)):
      redacted = dict(logs[i])
      redacted['textPayload'] = response.item.table.rows[i].values[0].string_value
      # you may consider changing insert ID if the project already has a copy
      # of this log (e.g. redacted['insertId'] = 'deid-' + redacted['insertId'])
      # For more details about insert ID, please see:
      # https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#FIELDS.insert_id
      modified_logs.append(redacted)

    yield modified_logs


class IngestLogs(DoFn):
  '''Ingest payloads into destination log'''

  def __init__(self, destination_log_name):
    self.destination_log_name = destination_log_name
    self.logger = None
  
  def _replace_log_name(self, entry):
    # update log name in the entry with destination log
    entry['logName'] = self.logger.name
    return entry

  def setup(self):
    # initialize logging client
    if self.logger:
      return

    logging_client = logging_v2.Client()
    if not logging_client:
      logging.error('Cannot create Google Logging Client')
      raise PipelineError('Cannot create Google Logging Client')
    self.logger = logging_client.logger(self.destination_log_name)
    if not self.logger:
      logging.error('Google client library cannot create Logger object')
      raise PipelineError('Google client library cannot create Logger object')

  def process(self, element):
    if self.logger:
      logs = list(map(self._replace_log_name, element))
      self.logger.client.logging_api.write_entries(logs)
    yield logs


def run(pubsub_subscription: str,
        destination_log_name: str,
        window_size: float,
        pipeline_args: List[str]=None) -> None:
  '''Runs Dataflow pipeline'''

  pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True
    )
  pipeline = Pipeline(options=pipeline_options)
  _ = (
    pipeline
    | 'Read log entries from Pub/Sub' >> io.ReadFromPubSub(subscription=pubsub_subscription)
    | 'Convert log entry payload to Json' >> ParDo(PayloadAsJson())
    | 'Aggregate payloads in fixed time intervals' >> WindowInto(FixedWindows(window_size))
    # Optimize Google API consumption and avoid possible throttling
    # by calling APIs for batched data and not per each element
    | 'Batch aggregated payloads' >> CombineGlobally(BatchPayloads()).without_defaults()
    # TODO: Add redaction logic here
    | 'Ingest to output log' >> ParDo(IngestLogs(destination_log_name))
  )
  pipeline.run()


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--input_pubsub_subscription',
      help='The Cloud Pub/Sub subscription to read from in the format '
      '"projects/<PROJECT_ID>/subscription/<SUBSCRIPTION_ID>".',
  )
  parser.add_argument(
      '--output_log_name',
      help='The log name to ingest log entries in the format '
      '"projects/<PROJECT_ID>/logs/<LOG_ID>".',
  )
  parser.add_argument(
      '--window_size',
      type=float,
      default=60.0,
      help='Output file\'s window size in seconds.',
  )
  known_args, pipeline_args = parser.parse_known_args()

  run(
      known_args.input_pubsub_subscription,
      known_args.output_log_name,
      known_args.window_size,
      pipeline_args,
  )

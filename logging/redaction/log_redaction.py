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

from apache_beam import CombineFn, CombineGlobally, DoFn, FixedWindow, io, ParDo, WindowInto
from apache_beam.error import PipelineError
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import logging_v2


class PayloadAsJson(DoFn):
  """Convert PubSub message payload to UTF-8 and return as Json"""

  def process(self, element):
    element.decode("utf-8")
    yield (
        json.loads(element.decode("utf-8"))
    )


class BatchPayloads(CombineFn):
  """Opinionated way to batch all payloads in the window"""

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


class IngestLogs(DoFn):
  """Ingest payloads into destination log"""

  def __init__(self, destination_log_name):
    logging_client = logging_v2.Client()
    if not logging_client:
      logging.error("Cannot create GCP Logging Client")
      raise PipelineError("Cannot create GCP Logging Client")
    self.logger = gcp_logging_client.logger(destination_log_name)
    if not self.logger:
      logging.error("Google client library cannot create Logger object")
      raise PipelineError("Google client library cannot create Logger object")
  
  def process(self, element):
    def replace_log_name(entry):
      entrylog['logName'] = self.logger.name
      return entry
    
    # replace 'original' log name with destination log name
    logs = list(map(replace_log_name, element))
    self.logger.client.logging_api.write_entries(logs)
    yield logs


def run(input_subscription: str,
        output_log_name: str,
        window_size: float,
        pipeline_args: List[str]=None) -> None:
  """Runs Dataflow pipeline"""
  pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True
    )
  pipeline = beam.Pipeline(options=pipeline_options)
  _ = (
    pipeline
    | "Read log entries from Pub/Sub" >> io.ReadFromPubSub(subscription=input_subscription)
    | "Convert log entry payload to Json" >> ParDo(PayloadAsJson())
    | "Aggregate payloads in fixed time intervals" >> WindowInto(FixedWindows(window_size))
    # Optimize Google API consumption and avoid possible throttling
    # by calling APIs for batched data and not per each element
    | "Batch aggregated payloads" >> CombineGlobally(BatchPayloads())
    # TODO: Add redaction logic here
    | "Ingest to output log" >> ParDo(IngestLogs(output_log_name))
  )


if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)

  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--input_subscription",
      help="The Cloud Pub/Sub subscription to read from in the format "
      '"projects/<PROJECT_ID>/subscription/<SUBSCRIPTION_ID>".',
  )
  parser.add_argument(
      "--output_log_name",
      help="The log name to ingest log entries in the format "
      '"projects/<PROJECT_ID>/logs/<LOG_ID>".',
  )
  parser.add_argument(
      "--window_size",
      type=float,
      default=60.0,
      help="Output file's window size in seconds.",
  )
  known_args, pipeline_args = parser.parse_known_args()

  run(
      known_args.input_subscription,
      known_args.output_log_name,
      known_args.window_size,
      pipeline_args,
  )

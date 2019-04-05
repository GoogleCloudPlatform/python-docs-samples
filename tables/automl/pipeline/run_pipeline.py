# Copyright 2019 Google Inc. All Rights Reserved.
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import logging
import argparse

import tables_config
import tables_client
import tables_pipeline


def parse_arguments(argv):
  """Parses command line arguments."""

  parser = argparse.ArgumentParser(description='Args for Tables pipeline.')
  parser.add_argument(
      '--config_filename',
      required=True,
      type=str,
      help='The filepath for the YAML configuration file.')
  parser.add_argument(
      '--log_dir',
      required=False,
      type=str,
      help='The directory to generate a session log file in.')
  parser.add_argument(
      '--service_account_filename',
      required=False,
      type=str,
      help='The filepath for the json key for oath.')
  parser.add_argument(
      '--console_log_level',
      required=False,
      type=str,
      default=logging.WARN,
      help='Controls the log level for the console display.')
  parser.add_argument(
      '--file_log_level',
      required=False,
      type=str,
      default=logging.INFO,
      help='Controls the log level to write to file. Set to logging.DEBUG for'
           'to write out the full AutoML service responses (very verbose).')
  args, _ = parser.parse_known_args(args=argv[1:])

  # Parser for parameters to pass to TablesConfig
  param_parser = argparse.ArgumentParser(description='Args for config params.')

  # Resource parameters
  param_parser.add_argument(
      '--project',
      required=False,
      type=str,
      help='GCP project ID to run AutoML Tables on.')
  param_parser.add_argument(
      '--location',
      required=False,
      default='us-central1',
      type=str,
      help='GCP location to run AutoML Tables in.')

  # Runtime parameters
  param_parser.add_argument(
      '--build_dataset',
      action='store_const',
      const=True,
      help='Builds a new dataset, loads an old dataset otherwise.')
  param_parser.add_argument(
      '--build_model',
      action='store_const',
      const=True,
      help='Builds a new model, loads an old model otherwise.')
  param_parser.add_argument(
      '--make_prediction',
      action='store_const',
      const=True,
      help='Makes a batch prediction.')

  # Dataset parameters
  # Note that columns_dtype and columns_nullable must be set in YAML config.
  param_parser.add_argument(
      '--dataset_display_name',
      required=False,
      type=str,
      help='Name of the Tables Dataset (32 character max).')
  param_parser.add_argument(
      '--dataset_input_path',
      required=False,
      type=str,
      help=('Path to import the training data from, one of'
            'bq://project.dataset.table or gs://path/to/csv'))
  param_parser.add_argument(
      '--label_column',
      required=False,
      type=str,
      help='Label to to train model on, for regression or classification.')
  param_parser.add_argument(
      '--split_column',
      required=False,
      type=str,
      help='Explicitly defines "TRAIN"/"VALIDATION"/"TEST" split.')
  param_parser.add_argument(
      '--weight_column',
      required=False,
      type=str,
      help='Weights loss and metrics.')
  param_parser.add_argument(
      '--time_column',
      required=False,
      type=str,
      help='Date/timestamp to automatically split data on.')

  # Model parameters
  # Note that ignore columns must be set in YAML config.
  param_parser.add_argument(
      '--model_display_name',
      required=False,
      type=str,
      help='Name of the Tables Model (32 character max).')
  param_parser.add_argument(
      '--train_hours',
      required=False,
      type=float,
      help='The number of hours to train the model for.')
  param_parser.add_argument(
      '--optimization_objective',
      required=False,
      type=str,
      help='Metric to optimize for in training.')

  # Predict parameters
  param_parser.add_argument(
      '--predict_input_path',
      required=False,
      type=str,
      help=('Path to import the batch prediction data from, one of'
            'bq://project.dataset.table or gs://path/to/csv'))
  param_parser.add_argument(
      '--predict_output_path',
      required=False,
      type=str,
      help=('Path to export batch predictions to, one of'
            'bq://project or gs://path'))
  params, _ = param_parser.parse_known_args(args=argv[1:])
  return args, params


def main():
  args, params = parse_arguments(sys.argv)
  config = tables_config.TablesConfig(args.config_filename, vars(params))
  client = tables_client.TablesClient(args.service_account_filename)
  pipeline = tables_pipeline.TablesPipeline(
      tables_config=config,
      tables_client=client,
      log_dir=args.log_dir,
      console_log_level=args.console_log_level,
      file_log_level=args.file_log_level)
  pipeline.run()


if __name__ == '__main__':
  main()

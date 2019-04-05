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

import functools

import yaml


class TablesConfig(object):
  """ Manage parameters to configure AutoML Tables training jobs.

  Args:
    config_filename: Absolute path for YAML config file to read from.
    args: dict of params to override config, ex. from command line args.

  Params:
    project: GCP project ID to run AutoML Tables on.
    location: GCP location to run AutoML Tables in.

    build_dataset: Builds a new dataset if True, loads an old dataset if False.
    build_model: Builds a new model if True, loads an old model if False.
    make_prediction: Makes a batch prediction if True.

    dataset_display_name: Name of the Tables Dataset (32 character max).
    dataset_input_path: Path to import the training data from, one of
        bq://project.dataset.table or gs://path/to/csv
    label_column: Label to train model on, for regression or classification.
    split_column: Explicitly defines 'TRAIN'/'VALIDATION'/'TEST' split.
    weight_column: Weights loss and metrics.
    time_column: Date/timestamp to automatically split data on.
    columns_dtype: dict of column names with types (ex. 'FLOAT64', 'STRING').
    columns_nullable: dict of column names with bool for nullable.

    model_display_name: Name of the Tables Dataset (32 character max).
    train_hours: (float) The number of hours to train the model for.
    optimization_objective: Metric to optimize for in training.
    ignore_columns: List of column display names to exclude from training, note
        that label, split, and weight columns will be excluded.

    predict_input_path: Path to import batch prediction data from, one of
        bq://project.dataset.table or gs://path/to/csv
    predict_output_path: Path to export batch predictions to, one of
        bq://project or gs://path

    See cloud.google.com/automl-tables/docs/ for more details, some parameters
    are modified for TablesClient to simplify specification. See below for
    which parameters are optional.

  Parameters common across multiple training jobs can be defined in a
  YAML config file, and parameters such as display names may be provided on a
  run by run basis. Parameters can be written to a new config file to track
  parameters passed in as arguments (ex. from the command line).
  """

  def __init__(self, config_filename, args=None):
    args = args if args is not None else {}
    config = self.params_from_file(config_filename)
    set_param = functools.partial(self._set_param, config=config, args=args)

    # Resource parameters.
    set_param('project', required=True)
    set_param('location', default='us-central1')

    # Runtime parameters
    set_param('build_dataset', default=False)
    set_param('build_model', default=False)
    set_param('make_prediction', default=False)

    # Dataset parameters.
    set_param('dataset_display_name', required=True)
    set_param('dataset_input_path', required=True)
    set_param('label_column', required=True)
    set_param('split_column')
    set_param('weight_column')
    set_param('time_column')
    set_param('columns_dtype')
    set_param('columns_nullable')

    # Model parameters.
    set_param('model_display_name', required=True)
    set_param('train_hours', default=1.0)
    set_param('optimization_objective')
    set_param('ignore_columns')

    # Predict parameters.
    set_param('predict_input_path')
    set_param('predict_output_path')

  def _set_param(self, key, config, args, required=False, default=None):
    """ Sets parameters, prioritizing those passed as arguments.

    Args:
      key: attribute name for the parameter, must match for arg and config.
      config: dict of params read from configuration file.
      args: dict of params to override or complement those from the config file.
      required: When True, raise an error if the param is None.
      default: If the param is None, replace with default.
    """
    param = args.get(key) if args.get(key) is not None else config.get(key)
    if param is None:
      if required:
        raise ValueError('{} must be defined.'.format(key))
      if default is not None:
        param = default
    setattr(self, key, param)

  def params_from_file(self, config_filename):
    """ Reads parameters from a YAML config file.

    Args:
      config_filename: Absolute path for YAML config file to read from.
    """
    with open(config_filename, 'r') as f:
      params = yaml.load(f, Loader=yaml.Loader)
    return params

  def params_to_file(self, config_filename):
    """ Writes parameters to a YAML config file.

    Args:
      config_filename: Absolute path for YAML config file to write to.
    """
    params = vars(self)
    with open(config_filename, 'w') as f:
      yaml.dump(params, f, default_flow_style=False)

  def params_to_printout(self):
    """ Returns parameters in YAML formatted printout.

    Returns:
      YAML dump of config.
    """
    params = vars(self)
    return yaml.dump(params, default_flow_style=False)

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

import os
import logging
import datetime


class TablesPipeline(object):
  """ Executes AutoML Tables operations to train models with logging.

  Args:
    tables_config: TablesConfig instance with pipeline parameters.
    tables_client: TablesClient instance with authentication credentials.
    console_log_level: Log level for console printout, WARN by default.
    file_log_level: Log level for log file writeouts, INFO by default.
    log_dir: Where log files are written to, defaults to current_dir/log.

  TablesPipeline can either load previously imported/trained datasets/models, or
  build new ones using parameters from tables_config, then optionally runs a
  batch prediction job. The pipeline loads datasets and models using their
  display names for convenience.
  """
  def __init__(self,
               tables_config,
               tables_client,
               console_log_level=logging.WARN,
               file_log_level=logging.INFO,
               log_dir=None):

    self.config = tables_config
    self.client = tables_client
    self.logger = self._get_logger(console_log_level,
                                   file_log_level,
                                   log_dir)

    # TODO: Extract from (non-unique) display_names.
    # AutoML operation names, capture during load/build dataset/model.
    self.dataset_name = None
    self.model_name = None

    self.logger.info("Tables configuration: \n{}".format(
        self.config.params_to_printout()))


  def _get_logger(self, console_log_level, file_log_level, log_dir=None):
    """ Gets a Logger with file and console log handlers.

    Args:
      console_log_level: Log level for console printout.
      file_log_level: Log level for log file writeouts.
      log_dir: Where log files are written to, defaults to current_dir/log.

    Log names are derived from dataset + model + timestamp.
    """
    if not log_dir:
      log_dir = os.path.join(os.getcwd(), 'log')
    # Truncate datetime to milliseconds.
    now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")[:-3]
    log_name = '_'.join([self.config.dataset_display_name,
                         self.config.model_display_name,
                         now])
    log_path = os.path.join(log_dir, log_name + '.log')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(file_log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

  def load_dataset(self):
    """ Loads a previously created dataset from display name.

    Note: will load the most recent dataset when there are multiple with the
    same display name.
    """
    print('Loading dataset...')
    datasets = self.client.list_datasets_by_display_name(
        self.config.project,
        self.config.location,
        self.config.dataset_display_name)
    print(len(datasets))
    try:
      if not datasets:
        raise NameError("Dataset with display name {} not found.".format(
            self.config.dataset_display_name))
      elif len(datasets) > 1:
        dataset = datasets[0] # Ordered by create time by default.
        self.logger.warn('Multiple Datasets found for display name {}, '
                         'loading the most recently created one.'.format(
                          self.config.dataset_display_name))
      else:
        dataset = datasets[0]
    except:
      self.logger.error('Failed to load dataset, see log for details.',
          exc_info=True)
      raise
    # TODO: Check dataset for label and stats update.
    print('Dataset Loaded.\n')
    self.dataset_name = dataset.name
    self.logger.info("Dataset name: {}".format(self.dataset_name))

  def load_model(self):
    """ Loads a previously created model from display name.

    Note: will load the most recent model when there are multiple with the
    same display name.
    Logs a summary of evaluation metrics.
    """
    print('Loading Model...')
    models = self.client.list_models_by_display_name(
        self.config.project,
        self.config.location,
        self.config.model_display_name)
    try:
      if not models:
        raise NameError("Model with display name {} not found.".format(
            self.config.model_display_name))
      elif len(models) > 1:
        model = models[0] # Ordered by create time by default.
        self.logger.warn('Multiple models found for display name {}, '
                         'loading the most recently created one.'.format(
                          self.config.model_display_name))
      else:
        model = models[0]
    except:
      self.logger.error('Failed to load dataset, see log for details.',
          exc_info=True)
      raise

    print('Model Loaded.\n')
    self.model_name = model.name
    self.logger.info("Model name: {}".format(self.model_name))

    metrics = self.client.model_evaluation(self.model_name)
    print("Model evaluation metrics: \n{}".format(metrics))
    self.logger.info("Model evaluation metrics: \n{}".format(metrics))

    feature_importance = self.client.feature_importance(self.model_name)
    print("Model feature importance: \n{}".format(feature_importance))
    self.logger.info("Model feature importance: \n{}".format
      (feature_importance))

  def build_dataset(self):
    """ Builds a new dataset based on config parameters.

    Operations are executed and queued with synchronous waits, so this function
    returns only after the final dataset update is complete.

    Note: will create a new dataset even if there exists one with the same
    display name.
    """
    print('Creating dataset...')
    try:
      create_dataset_response = self.client.create_dataset(
          self.config.project,
          self.config.location,
          self.config.dataset_display_name)
      print('Dataset created.\n')
      self.logger.debug(create_dataset_response)
      self.dataset_name = create_dataset_response.name
    except:
      self.logger.error(
          'Failed to create dataset, see log for details.', exc_info=True)
      raise

    print('Importing dataset...')
    try:
      import_data_response = self.client.import_data(
          self.dataset_name,
          self.config.dataset_input_path)
      self.logger.info('Import data operation name: \n{}'.format(
          import_data_response.operation.name))

      import_data_result = import_data_response.result()
      self.logger.debug(import_data_result)
      print('Dataset imported.\n')
    except:
      self.logger.error(
          'Failed to import data, see log for details.', exc_info=True)
      raise

    print('Updating dataset...')
    try:
      update_dataset_response = self.client.update_dataset(
          self.dataset_name,
          self.config.label_column,
          self.config.split_column,
          self.config.weight_column,
          self.config.time_column,
          self.config.columns_dtype,
          self.config.columns_nullable)
      # Not separated by operation type, only log for debugging
      self.logger.debug(update_dataset_response)
      print('Dataset updated.\n')
    except:
      self.logger.error(
          'Failed to update dataset, see log for details.', exc_info=True)
      raise
    self.logger.info("Dataset name: {}".format(self.dataset_name))

  def build_model(self):
    """ Builds a new model based on config parameters.

    Operations are executed and queued with synchronous waits, so this function
    returns only after the model evaluation is complete (and logged).

    Note: will create a new dataset even if there exists one with the same
    display name.
    """
    print('Creating model...')
    try:
      create_model_response = self.client.create_model(
          self.config.project,
          self.config.location,
          self.dataset_name,
          self.config.model_display_name,
          self.config.train_hours,
          self.config.optimization_objective,
          self.config.ignore_columns)
      self.logger.info('Create model operation name: \n{}'.format(
          create_model_response.operation.name))

      create_model_result = create_model_response.result()
      self.logger.debug(create_model_result)
      print('Model created.\n')

      self.model_name = create_model_result.name
      self.logger.info("Model name: {}".format(self.model_name))

      metrics = self.client.model_evaluation(self.model_name)
      print("Model evaluation metrics: \n{}".format(metrics))
      self.logger.info("Model evaluation metrics: \n{}".format(metrics))

      feature_importance = self.client.feature_importance(self.model_name)
      print("Model feature importance: \n{}".format(feature_importance))
      self.logger.info("Model feature importance: \n{}".format
        (feature_importance))
    except:
      self.logger.error(
          'Failed to create model, see log for details.', exc_info=True)
      raise

  def make_prediction(self):
    """ Makes predictions for the prediction input data in the config.

    Operations are executed and queued with synchronous waits, so this function
    returns only after the prediction export is complete.

    Note: The prediction export location is logged for easier retrieval, as the
    directory/dataset is automatically generated with a timestamp at run time.
    """
    print('Making batch prediction...')
    try:
      batch_predict_response = self.client.batch_predict(
          self.model_name,
          self.config.predict_input_path,
          self.config.predict_output_path)
      self.logger.info('Batch prediction operation name: \n{}'.format(
          batch_predict_response.operation.name))

      try:
        batch_predict_result = batch_predict_response.result()
      except:
        # Hides Any to BatchPredictResult conversion error in client (bug).
        pass
      print('Batch prediction complete.\n')
      output_info = (batch_predict_response.metadata.batch_predict_details.
                     output_info)

      self.logger.info('Batch prediction output location: \n{}'.format(
          output_info))
    except:
      self.logger.error(
          'Failed to make a batch prediction, see log for details.',
          exc_info=True)
      raise

  def run(self):
    """Runs pipeline and creates logs for debugging and record keeping.

    The pipeline is specified by config parameters, but the operations can be
    called directly from the TablesPipeline if a different pattern is required.
    """
    if self.config.build_dataset is True:
      self.build_dataset()
    else:
      self.load_dataset()

    if self.config.build_model is True:
      self.build_model()
    else:
      self.load_model()

    if self.config.make_prediction:
      self.make_prediction()

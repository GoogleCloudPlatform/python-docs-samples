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

# Note: this import needs to be modified upon new release.
from google.cloud import automl_v1beta1 as automl

class TablesClient(object):
  """ Wraps the AutoML Python client and adds helper functions.

  Args:
    service_account_filename: Path of json key for authentication, will use
    GOOGLE_APPLLICATION_CREDENTIALS if not set.

  AutoML client takes nested dictionaries for datasets, models, etc. matching
  the structures used by the service, the primary function of this wrapper is to
  build these nested dictionaries directly from the inputs. Some arguments are
  also changed to make them easier to specify in config files.
  """
  def __init__(self, service_account_filename=None):
    if service_account_filename:
      self.client = automl.AutoMlClient.from_service_account_file(
          filename=service_account_filename)
      self.prediction_client = (
          automl.PredictionServiceClient.from_service_account_file(
              filename=service_account_filename))
    else:
      # AutoML client uses two clients, one for training, one for prediction.
      self.client = automl.AutoMlClient()
      self.prediction_client = automl.PredictionServiceClient()

  def list_datasets_by_display_name(self, project, location, display_name):
    """ Lists all datasets with the specified display name.

    Args:
      project: GCP project ID.
      location: GCP compute resource location.
      display_name: Dataset display name.
    Returns:
      List of datasets.
    """
    parent = self.client.location_path(project, location)
    dataset_filter = 'display_name={}'.format(display_name)
    response = self.client.list_datasets(parent, dataset_filter)
    return list(response)

  def list_models_by_display_name(self, project, location, display_name):
    """ Lists all models with the specified display name.

    Args:
      project: GCP project ID.
      location: GCP compute resource location.
      display_name: Model display name.
    Returns:
      List of Models.
    """
    parent = self.client.location_path(project, location)
    model_filter = 'display_name={}'.format(display_name)
    response = self.client.list_models(parent, model_filter)
    return list(response)

  def get_primary_table_spec(self, dataset_name):
    """ Get the table spec for the primary table.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name).
    Returns:
      Table spec for the primary table.
    """
    list_table_specs_response = self.client.list_table_specs(dataset_name)
    return list(list_table_specs_response)[0] # Primary table is index 0.

  def get_column_specs(self, dataset_name):
    """ Get a dictionary mapping column display names to column specs.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name).
    Returns:
      Dict with column_display_name: column_spec.
    """
    primary_table_name = self.get_primary_table_spec(dataset_name).name
    list_column_specs_response = self.client.list_column_specs(
        primary_table_name)
    return {s.display_name: s for s in list_column_specs_response}

  def get_id(self, name):
    """ Extracts ID from full ID for AutoML service."""
    return name.rsplit('/', 1)[-1]

  def column_id(self, display_name, column_specs):
    """ Extracts ID for AutoML service with full column display name."""
    return self.get_id(column_specs[display_name].name)

  def create_dataset(self,
                     project,
                     location,
                     dataset_display_name):
    """ Creates a new AutoML Tables dataset.

    Args:
      project: GCP project ID.
      location: GCP compute resource location.
      dataset_display_name: User readable name for the dataset (32 char max).

    Returns:
      A dataset.
    """
    parent = self.client.location_path(project, location)
    dataset = {
        'display_name': dataset_display_name,
        'tables_dataset_metadata': {},
    }
    return self.client.create_dataset(parent=parent, dataset=dataset)

  def import_data(self, dataset_name, dataset_input_path):
    """ Imports data into a dataset from BigQuery or Cloud Storage.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name).
      dataset_input_path: Path to import the training data from, one of
          bq://project.dataset.table or gs://path/to/csv

    Returns:
      An import data operation, that can be queried for metadata and completion
      status.
    """
    if dataset_input_path.startswith('bq'):
      input_config = {"bigquery_source": {"input_uri": dataset_input_path}}
    else:
      input_uris = dataset_input_path.split(",")
      input_config = {"gcs_source": {"input_uris": input_uris}}

    return self.client.import_data(dataset_name, input_config)

  def update_primary_table(self,
                           dataset_name,
                           time_column):
    """ Updates the primary table spec of a dataset.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name).
      time_column: Date/timestamp to automatically split data on.

    Returns:
      The updated primary table spec.
    """
    primary_table_name = self.get_primary_table_spec(dataset_name).name
    column_specs = self.get_column_specs(dataset_name)
    primary_table_spec = {
        'name': primary_table_name,
        'time_column_spec_id': self.column_id(time_column, column_specs),
    }
    return self.client.update_table_spec(primary_table_spec)

  def update_columns(self,
                     dataset_name,
                     columns_dtype=None,
                     columns_nullable=None):
    """ Updates the columns for the primary table spec of a dataset.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name).
      columns_dtype: dict of column names with types (ex. 'FLOAT64', 'STRING').
      columns_nullable: dict of column names with bool for nullable.

    Returns:
      List of (only the) updated column specs.
    """
    responses = []
    column_specs = self.get_column_specs(dataset_name)
    dtype_keys = list(columns_dtype.keys()) if columns_dtype else []
    nullable_keys = list(columns_nullable.keys()) if columns_nullable else []
    for display_name in set(dtype_keys + nullable_keys):
      # type_code is a required field, so it must be retrieved if not set.
      column_spec = column_specs[display_name]
      data_type = {
          'nullable': column_spec.data_type.nullable,
          'type_code': column_spec.data_type.type_code,
      }
      if display_name in dtype_keys:
        data_type['type_code'] = columns_dtype[display_name]
      if display_name in nullable_keys:
        data_type['nullable'] = columns_nullable[display_name]
      column_spec = {
          'name': column_spec.name,
          'data_type': data_type,
      }
      responses.append(self.client.update_column_spec(column_spec))
    return responses

  def update_dataset(self,
                     dataset_name,
                     label_column=None,
                     split_column=None,
                     weight_column=None,
                     time_column=None,
                     columns_dtype=None,
                     columns_nullable=None):
    """ Updates a dataset, as well as the primary table and columns it contains.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name).
      label_column: Label to train model on, for regression or classification.
      split_column: Explicitly defines 'TRAIN'/'VALIDATION'/'TEST' split.
      weight_column: Weights loss and metrics.
      time_column: Date/timestamp to automatically split data on.
      columns_dtype: dict of column names with types (ex. 'FLOAT64', 'STRING').
      columns_nullable: dict of column names with bool for nullable.

    Returns:
      List of (only the) updated column specs, primary table specs, dataset.

    AutoML client update dataset only updates the dataset, since it is
    usually run in tandem with update table spec and column spec, it is included
    here as one function.
    """
    responses = []

    if columns_dtype or columns_nullable:
      update_columns_responses = self.update_columns(
          dataset_name, columns_dtype, columns_nullable)
      responses.extend(update_columns_responses)

    if time_column:
      update_table_spec_response = self.update_primary_table(
          dataset_name, time_column)
      responses.append(update_table_spec_response)

    column_specs = self.get_column_specs(dataset_name)
    tables_dataset_metadata = {}
    if label_column:
      tables_dataset_metadata['target_column_spec_id'] = self.column_id(
          label_column, column_specs)
    if weight_column:
      tables_dataset_metadata['weight_column_spec_id'] = self.column_id(
          weight_column, column_specs)
    if split_column:
      tables_dataset_metadata['ml_use_column_spec_id'] = self.column_id(
          split_column, column_specs)
    dataset = {
        'name': dataset_name,
        'tables_dataset_metadata': tables_dataset_metadata
    }
    update_dataset_response = self.client.update_dataset(dataset=dataset)
    responses.append(update_dataset_response)
    return responses

  def create_model(self,
                   project,
                   location,
                   dataset_name,
                   model_display_name,
                   train_hours,
                   optimization_objective=None,
                   ignore_columns=None):
    """ Creates a new AutoML Tables model.

    Args:
      project: GCP project ID.
      location: GCP compute resource location.
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name) to use for training.
      model_display_name: User readable name for the model (32 char max).
      train_hours: (float) The number of hours to train the model for.
      optimization_objective: Metric to optimize for in training.
      ignore_columns: List of column display names to exclude from training,
          note that label, split, and weight columns will be excluded.

    Returns:
      A create model operation, that can be queried for metadata and completion
      status.
    """
    # Initialize model metadata, train budget is a required field.
    tables_model_metadata = {
        'train_budget_milli_node_hours': int(1000 * train_hours),
    }

    if optimization_objective:
      tables_model_metadata['optimization_objective'] = optimization_objective

    dataset = self.client.get_dataset(dataset_name)
    column_specs = self.get_column_specs(dataset_name)

    if ignore_columns:
      # Model feature columns must not include label, weight, or split.
      weight_id = str(dataset.tables_dataset_metadata.weight_column_spec_id)
      split_id = str(dataset.tables_dataset_metadata.ml_use_column_spec_id)
      label_id = str(dataset.tables_dataset_metadata.target_column_spec_id)
      input_feature_column_specs = [
          v for k, v in column_specs.items()
          if not k in ignore_columns
          and self.get_id(v.name) not in (weight_id, split_id, label_id)
      ]
      tables_model_metadata.update(
          {'input_feature_column_specs': input_feature_column_specs})

    model = {
        'display_name': model_display_name,
        'dataset_id': self.get_id(dataset_name),
        'tables_model_metadata': tables_model_metadata,
    }
    parent = self.client.location_path(project, location)
    return self.client.create_model(parent=parent, model=model)

  def model_evaluation(self, model_name):
    """ Creates a summary of model evaluation metrics.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name) to use for training.

    Returns:
      A string with evaluation metrics for printout.
    """
    response = self.client.list_model_evaluations(model_name)

    for evaluation in response:
      # Retrieve model evaluation and ignore evaluations for sclasses.
      if not evaluation.annotation_spec_id:
        model_evaluation_name = evaluation.name

    model_evaluation = self.client.get_model_evaluation(model_evaluation_name)

    classification_metrics = model_evaluation.classification_evaluation_metrics
    printout = ''
    if str(classification_metrics):
      printout += '(threshold at 0.5)\n'
      confidence_metrics = classification_metrics.confidence_metrics_entry
      for confidence_metric in confidence_metrics:
        if confidence_metric.confidence_threshold == 0.5:
          printout += '{:<10s}{:<0.4f} \n'.format(
              'Precision', confidence_metric.precision)
          printout += '{:<10s}{:<0.4f} \n'.format(
              'Recall', confidence_metric.recall)
          printout += '{:<10s}{:<0.4f} \n'.format(
              'F1 score', confidence_metric.f1_score)
      printout += '{:<10s}{:<0.4f}\n'.format(
          'AUPRC', classification_metrics.au_prc)
      printout += '{:<10s}{:<0.4f}\n'.format(
          'AUROC', classification_metrics.au_roc)
      printout += '{:<10s}{:<0.5}\n'.format(
          'Log loss', classification_metrics.log_loss)

    regression_metrics = model_evaluation.regression_evaluation_metrics
    if str(regression_metrics):
      printout += 'Regression metrics:\n'
      printout += '{:<10s}{:<0.5}\n'.format(
          'RMSE', regression_metrics.root_mean_squared_error)
      printout += '{:<10s}{:<0.5}\n'.format(
          'MAE', regression_metrics.mean_absolute_error)
      printout += '{:<10s}{:<0.5}\n'.format(
          'MAPE', regression_metrics.mean_absolute_percentage_error)
      printout += '{:<10s}{:<0.5}\n'.format(
          'R^2', regression_metrics.r_squared)
    return printout

  def feature_importance(self, model_name, display_number=10):
    """ Creates a summary of model feature importance.

    Args:
      dataset_name: Full ID for the dataset object on the AutoML service (not
          display name) to use for training.
      display_number: Number of top columns to display.

    Returns:
      A string with feature importance for printout.
    """
    model = self.client.get_model(model_name)
    column_info = model.tables_model_metadata.tables_model_column_info
    features = [(c.feature_importance, c.column_display_name)
                 for c in column_info]
    features.sort(reverse=True)
    printout = ''
    for importance, feature in features[:display_number]:
      printout += '{:<8.4f}{:<s}\n'.format(importance, feature)
    return printout

  def batch_predict(self, model_name, input_path, output_path):
    """ Make a batch of predictions.

    Args:
      input_path = 'gs://path/to/csv' or 'bq://project.dataset.table'
      output_path = 'gs://path' or `bq://project_id

    Returns:
      A batch predict operation, that can be queried for metadata and completion
      status.
    """
    if input_path.startswith('bq'):
      input_config = {"bigquery_source": {"input_uri": input_path}}
    else:
      # Get the multiple Google Cloud Storage URIs.
      input_uris = input_path.split(",").strip()
      input_config = {"gcs_source": {"input_uris": input_uris}}

    if output_path.startswith('bq'):
      output_config = {"bigquery_destination": {"output_uri": output_path}}
    else:
      output_config = {"gcs_destination": {"output_uri_prefix": output_path}}

    return self.prediction_client.batch_predict(
        model_name, input_config, output_config)

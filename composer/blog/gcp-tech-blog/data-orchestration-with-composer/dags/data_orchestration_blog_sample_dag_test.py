# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from airflow import models
import internal_unit_testing
import pytest

# user should substitute their project ID
PROJECT_ID = 'your-project-id'
BUCKET_NAME = 'your-bucket-name'
DATA_FILE_NAME = 'gcs://tbc'
DATASET = 'your-output-dataset'
TABLE = 'your-output-table'


@pytest.fixture(autouse=True, scope="function")
# The fixture `airflow_database` lives in composer/conftest.py.
def set_variables(airflow_database):
    models.Variable.set('gcp_project', PROJECT_ID)
    models.Variable.set('bucket_name', BUCKET_NAME)
    models.Variable.set('file_name', DATA_FILE_NAME)
    models.Variable.set('bigquery_dataset', DATASET)
    models.Variable.set('bigquery_table', TABLE)
    yield
    models.Variable.delete('gcp_project')
    models.Variable.delete('bucket_name')
    models.Variable.delete('file_name')
    models.Variable.delete('bigquery_dataset')
    models.Variable.delete('bigquery_table')

def test_dag_import():
    from . import data_orchestration_blog_sample_dag
    internal_unit_testing.assert_has_valid_dag(data_orchestration_blog_sample_dag)

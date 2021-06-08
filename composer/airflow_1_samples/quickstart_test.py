# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from airflow import models

import internal_unit_testing
import pytest


@pytest.fixture(autouse=True, scope="function")
# The fixture `airflow_database` lives in composer/conftest.py.
def set_variables(airflow_database):

    models.Variable.set('gcs_bucket', 'example_bucket')
    models.Variable.set('gcp_project', 'example-project')
    models.Variable.set('gce_zone', 'us-central1-f')
    yield
    models.Variable.delete('gcs_bucket')
    models.Variable.delete('gcp_project')
    models.Variable.delete('gce_zone')


def test_dag_import():
    """Test that the DAG file can be successfully imported.

    This tests that the DAG can be parsed, but does not run it in an Airflow
    environment. This is a recommended confidence check by the official Airflow
    docs: https://airflow.incubator.apache.org/tutorial.html#testing
    """

    from . import quickstart as module
    internal_unit_testing.assert_has_valid_dag(module)

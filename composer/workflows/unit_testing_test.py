# Copyright 2018 Google LLC
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

from airflow import exceptions
import pytest

from . import unit_testing


def test_dag_no_dag():
    from . import unit_testing as module  # Does not contain a DAG.
    with pytest.raises(AssertionError):
        unit_testing.assert_has_valid_dag(module)


def test_dag_has_cycle():
    from . import unit_testing_cycle as module
    with pytest.raises(exceptions.AirflowDagCycleException):
        unit_testing.assert_has_valid_dag(module)


# [START composer_dag_unit_testing]
def test_dag_with_variables():
    from airflow import models

    # Set any Airflow variables before importing the DAG module.
    models.Variable.set('gcp_project', 'example-project')

    # Importing the module verifies that there are no syntax errors.
    from . import unit_testing_variables as module

    # The assert_has_valid_dag verifies that the module contains an Airflow DAG
    # and that the DAG contains no cycles.
    unit_testing.assert_has_valid_dag(module)
# [END composer_dag_unit_testing]

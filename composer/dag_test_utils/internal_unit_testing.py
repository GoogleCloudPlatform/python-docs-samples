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

"""Utilities for unit testing DAGs."""

# [START composer_dag_unit_testing]
from airflow import models
from airflow.utils.dag_cycle_tester import test_cycle


def assert_has_valid_dag(module):
    """Assert that a module contains a valid DAG."""

    no_dag_found = True

    for dag in vars(module).values():
        if isinstance(dag, models.DAG):
            no_dag_found = False
            test_cycle(dag)  # Throws if a task cycle is found.

    if no_dag_found:
        raise AssertionError('module does not contain a valid DAG')
# [END composer_dag_unit_testing]

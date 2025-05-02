# Copyright 2025 Google LLC
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

from google.api_core.iam import Policy
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.table import Table

from view_table_or_view_access_policy import view_table_or_view_access_policy

EMPTY_POLICY_ETAG = "ACAB"


def test_view_dataset_access_policies_with_table(
    project_id: str,
    dataset: Dataset,
    table: Table,
) -> None:
    policy: Policy = view_table_or_view_access_policy(project_id, dataset.dataset_id, table.table_id)

    assert policy.etag == EMPTY_POLICY_ETAG
    assert not policy.bindings  # Empty bindings list


def test_view_dataset_access_policies_with_view(
    project_id: str,
    dataset: Dataset,
    view: Table,
) -> None:
    policy: Policy = view_table_or_view_access_policy(project_id, dataset.dataset_id, view.table_id)

    assert policy.etag == EMPTY_POLICY_ETAG
    assert not policy.bindings  # Empty bindings list

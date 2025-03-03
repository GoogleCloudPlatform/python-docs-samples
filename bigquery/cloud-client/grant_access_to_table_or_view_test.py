# Copyright 2025 Google LLC
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

from google.cloud import bigquery
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.table import Table

from grant_access_to_table_or_view import grant_access_to_table_or_view


def test_grant_access_to_table_or_view(
    client: bigquery.Client,
    dataset: Dataset,
    project_id: str,
    table: Table,
    entity_id: str,
) -> None:
    ROLE = "roles/bigquery.dataViewer"
    PRINCIPAL_ID = f"group:{entity_id}"

    empty_policy = client.get_iam_policy(table)

    # In an empty policy the role and principal is not present
    assert not any(p for p in empty_policy if p["role"] == ROLE)
    assert not any(p for p in empty_policy if PRINCIPAL_ID in p["members"])

    updated_policy = grant_access_to_table_or_view(
        project_id,
        dataset.dataset_id,
        table.table_id,
        principal_id=PRINCIPAL_ID,
        role=ROLE,
    )

    # A binding with that role exists
    assert any(p for p in updated_policy if p["role"] == ROLE)
    # A binding for that principal exists
    assert any(
        p for p in updated_policy
        if PRINCIPAL_ID in p["members"]
    )

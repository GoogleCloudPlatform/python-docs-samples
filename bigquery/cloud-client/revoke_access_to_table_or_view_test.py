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
from revoke_access_to_table_or_view import revoke_access_to_table_or_view


def test_revoke_access_to_table_or_view_for_role(
    client: bigquery.Client,
    dataset: Dataset,
    table: Table,
    entity_id: str,
) -> None:
    ROLE = "roles/bigquery.dataViewer"
    PRINCIPAL_ID = f"group:{entity_id}"

    empty_policy = client.get_iam_policy(table)
    assert not empty_policy.bindings

    policy_with_role = grant_access_to_table_or_view(
        dataset.project,
        dataset.dataset_id,
        table.table_id,
        principal_id=PRINCIPAL_ID,
        role=ROLE,
    )

    # Check that there is a binding with that role
    assert any(p for p in policy_with_role if p["role"] == ROLE)

    policy_with_revoked_role = revoke_access_to_table_or_view(
        dataset.project,
        dataset.dataset_id,
        resource_name=table.table_id,
        role_to_remove=ROLE,
    )

    # Check that this role is not present in the policy anymore
    assert not any(p for p in policy_with_revoked_role if p["role"] == ROLE)


def test_revoke_access_to_table_or_view_to_a_principal(
    client: bigquery.Client,
    dataset: Dataset,
    project_id: str,
    table: Table,
    entity_id: str,
) -> None:
    ROLE = "roles/bigquery.dataViewer"
    PRINCIPAL_ID = f"group:{entity_id}"

    empty_policy = client.get_iam_policy(table)

    # This binding list is empty
    assert not empty_policy.bindings

    updated_policy = grant_access_to_table_or_view(
        project_id,
        dataset.dataset_id,
        table.table_id,
        principal_id=PRINCIPAL_ID,
        role=ROLE,
    )

    # There is a binding for that principal.
    assert any(p for p in updated_policy if PRINCIPAL_ID in p["members"])

    policy_with_removed_principal = revoke_access_to_table_or_view(
        project_id,
        dataset.dataset_id,
        resource_name=table.table_id,
        principal_to_remove=PRINCIPAL_ID,
    )

    # This principal is not present in the policy anymore.
    assert not policy_with_removed_principal.bindings

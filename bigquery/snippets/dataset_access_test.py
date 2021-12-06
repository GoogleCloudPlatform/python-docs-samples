# Copyright 2021 Google LLC
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

import revoke_dataset_access
import update_dataset_access


def test_dataset_access_permissions(capsys, dataset_id, entity_id, bigquery_client):
    original_dataset = bigquery_client.get_dataset(dataset_id)
    update_dataset_access.update_dataset_access(dataset_id, entity_id)
    full_dataset_id = "{}.{}".format(
        original_dataset.project, original_dataset.dataset_id
    )

    out, err = capsys.readouterr()
    assert (
        "Updated dataset '{}' with modified user permissions.".format(full_dataset_id)
        in out
    )

    updated_dataset = bigquery_client.get_dataset(dataset_id)
    updated_dataset_entries = list(updated_dataset.access_entries)
    updated_dataset_entity_ids = {entry.entity_id for entry in updated_dataset_entries}
    assert entity_id in updated_dataset_entity_ids
    revoke_dataset_access.revoke_dataset_access(dataset_id, entity_id)
    revoked_dataset = bigquery_client.get_dataset(dataset_id)
    revoked_dataset_entries = list(revoked_dataset.access_entries)

    full_dataset_id = f"{updated_dataset.project}.{updated_dataset.dataset_id}"
    out, err = capsys.readouterr()
    assert (
        f"Revoked dataset access for '{entity_id}' to ' dataset '{full_dataset_id}.'"
        in out
    )
    assert len(revoked_dataset_entries) == len(updated_dataset_entries) - 1
    revoked_dataset_entity_ids = {entry.entity_id for entry in revoked_dataset_entries}
    assert entity_id not in revoked_dataset_entity_ids

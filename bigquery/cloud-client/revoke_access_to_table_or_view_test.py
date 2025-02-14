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

from google.cloud.bigquery.dataset import Dataset
# from google.cloud.bigquery.table import Table
# import os

# from revoke_access_to_table_or_view import revoke_access_to_table_or_view


def test_revoke_access_to_table_or_view(
    dataset: Dataset,
) -> None:
    pass
    # Incomplete test
    # table_policy = revoke_access_to_table_or_view(
    #     project_id=PROJECT_ID,
    #     dataset=dataset.dataset_id,
    #     resource_name=table.id,
    # )

    # updated_dataset_entity_ids = {entry.entity_id for entry in updated_dataset.access_entries}
    # assert ENTITY_ID in updated_dataset_entity_ids

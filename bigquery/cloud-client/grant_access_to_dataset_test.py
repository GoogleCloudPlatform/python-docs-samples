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

from grant_access_to_dataset import grant_access_to_dataset


def test_grant_access_to_dataset(
    dataset: Dataset,
    entity_id: str
) -> None:
    dataset_access_entries = grant_access_to_dataset(
        dataset_id=dataset.dataset_id,
        entity_id=entity_id,
        role="READER"
    )

    updated_dataset_entity_ids = {
        entry.entity_id for entry in dataset_access_entries
    }
    assert entity_id in updated_dataset_entity_ids

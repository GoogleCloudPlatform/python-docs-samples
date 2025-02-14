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

from google.cloud.bigquery.dataset import AccessEntry, Dataset

from view_dataset_access_policy import view_dataset_access_policy


def test_view_dataset_access_policies(
    dataset: Dataset,
) -> None:
    access_policy: list[AccessEntry] = view_dataset_access_policy(dataset.dataset_id)

    assert access_policy

# Copyright 2024 Google LLC
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


def test_create_iam_policy(table_id: str):
    your_table_id = table_id

    # [START bigquery_create_iam_policy]
    from google.cloud import bigquery

    bqclient = bigquery.Client()

    policy = bqclient.get_iam_policy(
        your_table_id,  # e.g. "project.dataset.table"
    )

    analyst_email = "example-analyst-group@google.com"
    binding = {
        "role": "roles/bigquery.dataViewer",
        "members": {f"group:{analyst_email}"},
    }
    policy.bindings.append(binding)

    updated_policy = bqclient.set_iam_policy(
        your_table_id,  # e.g. "project.dataset.table"
        policy,
    )

    for binding in updated_policy.bindings:
        print(repr(binding))
    # [END bigquery_create_iam_policy]

    assert binding in updated_policy.bindings

# Copyright 2020 Google LLC
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

import typing
from typing import Dict, Optional, Tuple

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


class OverridesDict(TypedDict, total=False):
    analyst_group_email: str
    view_dataset_id: str
    view_id: str
    view_reference: Dict[str, str]
    source_dataset_id: str
    source_id: str


def create_view(override_values: Optional[Dict[str, str]] = None) -> "bigquery.Table":
    if override_values is None:
        override_values = {}

    # [START bigquery_create_view]
    from google.cloud import bigquery

    client = bigquery.Client()

    view_id = "my-project.my_dataset.my_view"
    source_id = "my-project.my_dataset.my_table"
    # [END bigquery_create_view]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_id = override_values.get("view_id", view_id)
    source_id = override_values.get("source_id", source_id)
    # [START bigquery_create_view]
    view = bigquery.Table(view_id)

    # The source table in this example is created from a CSV file in Google
    # Cloud Storage located at
    # `gs://cloud-samples-data/bigquery/us-states/us-states.csv`. It contains
    # 50 US states, while the view returns only those states with names
    # starting with the letter 'W'.
    view.view_query = f"SELECT name, post_abbr FROM `{source_id}` WHERE name LIKE 'W%'"

    # Make an API request to create the view.
    view = client.create_table(view)
    print(f"Created {view.table_type}: {str(view.reference)}")
    # [END bigquery_create_view]
    return view


def get_view(override_values: Optional[Dict[str, str]] = None) -> "bigquery.Table":
    if override_values is None:
        override_values = {}

    # [START bigquery_get_view]
    from google.cloud import bigquery

    client = bigquery.Client()

    view_id = "my-project.my_dataset.my_view"
    # [END bigquery_get_view]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_id = override_values.get("view_id", view_id)
    # [START bigquery_get_view]
    # Make an API request to get the table resource.
    view = client.get_table(view_id)

    # Display view properties
    print(f"Retrieved {view.table_type}: {str(view.reference)}")
    print(f"View Query:\n{view.view_query}")
    # [END bigquery_get_view]
    return view


def update_view(override_values: Optional[Dict[str, str]] = None) -> "bigquery.Table":
    if override_values is None:
        override_values = {}

    # [START bigquery_update_view_query]
    from google.cloud import bigquery

    client = bigquery.Client()

    view_id = "my-project.my_dataset.my_view"
    source_id = "my-project.my_dataset.my_table"
    # [END bigquery_update_view_query]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_id = override_values.get("view_id", view_id)
    source_id = override_values.get("source_id", source_id)
    # [START bigquery_update_view_query]
    view = bigquery.Table(view_id)

    # The source table in this example is created from a CSV file in Google
    # Cloud Storage located at
    # `gs://cloud-samples-data/bigquery/us-states/us-states.csv`. It contains
    # 50 US states, while the view returns only those states with names
    # starting with the letter 'M'.
    view.view_query = f"SELECT name, post_abbr FROM `{source_id}` WHERE name LIKE 'M%'"

    # Make an API request to update the query property of the view.
    view = client.update_table(view, ["view_query"])
    print(f"Updated {view.table_type}: {str(view.reference)}")
    # [END bigquery_update_view_query]
    return view


def grant_access(
    override_values: Optional[OverridesDict] = None,
) -> Tuple["bigquery.Dataset", "bigquery.Dataset"]:
    if override_values is None:
        override_values = {}

    # [START bigquery_grant_view_access]
    from google.cloud import bigquery

    client = bigquery.Client()

    # To use a view, the analyst requires ACLs to both the view and the source
    # table. Create an authorized view to allow an analyst to use a view
    # without direct access permissions to the source table.
    view_dataset_id = "my-project.my_view_dataset"
    # [END bigquery_grant_view_access]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_dataset_id = override_values.get("view_dataset_id", view_dataset_id)
    # [START bigquery_grant_view_access]
    # Make an API request to get the view dataset ACLs.
    view_dataset = client.get_dataset(view_dataset_id)

    analyst_group_email = "data_analysts@example.com"
    # [END bigquery_grant_view_access]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    analyst_group_email = override_values.get(
        "analyst_group_email", analyst_group_email
    )
    # [START bigquery_grant_view_access]
    access_entries = view_dataset.access_entries
    access_entries.append(
        bigquery.AccessEntry("READER", "groupByEmail", analyst_group_email)
    )
    view_dataset.access_entries = access_entries

    # Make an API request to update the ACLs property of the view dataset.
    view_dataset = client.update_dataset(view_dataset, ["access_entries"])
    print(f"Access to view: {view_dataset.access_entries}")

    # Group members of "data_analysts@example.com" now have access to the view,
    # but they require access to the source table to use it. To remove this
    # restriction, authorize the view to access the source dataset.
    source_dataset_id = "my-project.my_source_dataset"
    # [END bigquery_grant_view_access]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    source_dataset_id = override_values.get("source_dataset_id", source_dataset_id)
    # [START bigquery_grant_view_access]
    # Make an API request to set the source dataset ACLs.
    source_dataset = client.get_dataset(source_dataset_id)

    view_reference = {
        "projectId": "my-project",
        "datasetId": "my_view_dataset",
        "tableId": "my_authorized_view",
    }
    # [END bigquery_grant_view_access]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_reference = override_values.get("view_reference", view_reference)
    # [START bigquery_grant_view_access]
    access_entries = source_dataset.access_entries
    access_entries.append(bigquery.AccessEntry(None, "view", view_reference))
    source_dataset.access_entries = access_entries

    # Make an API request to update the ACLs property of the source dataset.
    source_dataset = client.update_dataset(source_dataset, ["access_entries"])
    print(f"Access to source: {source_dataset.access_entries}")
    # [END bigquery_grant_view_access]
    return view_dataset, source_dataset

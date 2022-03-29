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
from typing import Dict, Optional

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def create_materialized_view(
    override_values: Optional[Dict[str, str]] = None
) -> "bigquery.Table":
    if override_values is None:
        override_values = {}

    # [START bigquery_create_materialized_view]
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()

    view_id = "my-project.my_dataset.my_materialized_view"
    base_table_id = "my-project.my_dataset.my_base_table"
    # [END bigquery_create_materialized_view]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_id = override_values.get("view_id", view_id)
    base_table_id = override_values.get("base_table_id", base_table_id)
    # [START bigquery_create_materialized_view]
    view = bigquery.Table(view_id)
    view.mview_query = f"""
    SELECT product_id, SUM(clicks) AS sum_clicks
    FROM  `{base_table_id}`
    GROUP BY 1
    """

    # Make an API request to create the materialized view.
    view = bigquery_client.create_table(view)
    print(f"Created {view.table_type}: {str(view.reference)}")
    # [END bigquery_create_materialized_view]
    return view


def update_materialized_view(
    override_values: Optional[Dict[str, str]] = None
) -> "bigquery.Table":
    if override_values is None:
        override_values = {}

    # [START bigquery_update_materialized_view]
    import datetime
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()

    view_id = "my-project.my_dataset.my_materialized_view"
    # [END bigquery_update_materialized_view]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_id = override_values.get("view_id", view_id)
    # [START bigquery_update_materialized_view]
    view = bigquery.Table(view_id)
    view.mview_enable_refresh = True
    view.mview_refresh_interval = datetime.timedelta(hours=1)

    # Make an API request to update the materialized view.
    view = bigquery_client.update_table(
        view,
        # Pass in a list of any fields you need to modify.
        ["mview_enable_refresh", "mview_refresh_interval"],
    )
    print(f"Updated {view.table_type}: {str(view.reference)}")
    # [END bigquery_update_materialized_view]
    return view


def delete_materialized_view(override_values: Optional[Dict[str, str]] = None) -> None:
    if override_values is None:
        override_values = {}

    # [START bigquery_delete_materialized_view]
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()

    view_id = "my-project.my_dataset.my_materialized_view"
    # [END bigquery_delete_materialized_view]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    view_id = override_values.get("view_id", view_id)
    # [START bigquery_delete_materialized_view]
    # Make an API request to delete the materialized view.
    bigquery_client.delete_table(view_id)
    # [END bigquery_delete_materialized_view]

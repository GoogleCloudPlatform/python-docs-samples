# Copyright 2021 Google LLC
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
#
# [START contactcenterinsights_export_to_bigquery]
from google.cloud import contact_center_insights_v1


def export_to_bigquery(
    project_id: str,
    bigquery_project_id: str,
    bigquery_dataset_id: str,
    bigquery_table_id: str,
) -> None:
    """Exports data to BigQuery.

    Args:
        project_id:
            The project identifier that owns the data source to be exported.
            For example, 'my-project'.
        bigquery_project_id:
            The project identifier that owns the BigQuery sink to export data to.
            For example, 'my-project'.
        bigquery_dataset_id:
            The BigQuery dataset identifier. For example, 'my-dataset'.
        bigquery_table_id:
            The BigQuery table identifier. For example, 'my-table'.

    Returns:
        None.
    """
    # Construct an export request.
    request = contact_center_insights_v1.ExportInsightsDataRequest()
    request.parent = (
        contact_center_insights_v1.ContactCenterInsightsClient.common_location_path(
            project_id, "us-central1"
        )
    )
    request.big_query_destination.project_id = bigquery_project_id
    request.big_query_destination.dataset = bigquery_dataset_id
    request.big_query_destination.table = bigquery_table_id
    request.filter = 'agent_id="007"'

    # Call the Insights client to export data to BigQuery.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    export_operation = insights_client.export_insights_data(request=request)
    export_operation.result(timeout=600000)
    print("Exported data to BigQuery")


# [END contactcenterinsights_export_to_bigquery]

#!/usr/bin/env python
#
# Copyright 2022 Google LLC
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

"""Snippets on exporting findings from Security Command Center to BigQuery."""


# [START securitycenter_create_bigquery_export]


def create_bigquery_export(
    parent: str, export_filter: str, bigquery_dataset_id: str, bigquery_export_id: str
):

    from google.cloud import securitycenter
    print('Triggering tests')
    """
    Create export configuration to export findings from a project to a BigQuery dataset.
    Optionally specify filter to export certain findings only.

    Args:
        parent: Use any one of the following resource paths:
             - organizations/{organization_id}
             - folders/{folder_id}
             - projects/{project_id}
        export_filter: Expression that defines the filter to apply across create/update events of findings.
        bigquery_dataset_id: The BigQuery dataset to write findings' updates to.
        bigquery_export_id: Unique identifier provided by the client.
             - example id: f"default-{str(uuid.uuid4()).split('-')[0]}"
        For more info, see:
        https://cloud.google.com/security-command-center/docs/how-to-analyze-findings-in-big-query#export_findings_from_to
    """
    client = securitycenter.SecurityCenterClient()

    # Create the BigQuery export configuration.
    bigquery_export = securitycenter.BigQueryExport()
    bigquery_export.description = "Export low and medium findings if the compute resource has an IAM anomalous grant"
    bigquery_export.filter = export_filter
    bigquery_export.dataset = f"{parent}/datasets/{bigquery_dataset_id}"

    request = securitycenter.CreateBigQueryExportRequest()
    request.parent = parent
    request.big_query_export = bigquery_export
    request.big_query_export_id = bigquery_export_id

    # Create the export request.
    response = client.create_big_query_export(request)

    print(f"BigQuery export request created successfully: {response.name}\n")


# [END securitycenter_create_bigquery_export]


# [START securitycenter_get_bigquery_export]
def get_bigquery_export(parent: str, bigquery_export_id: str):
    from google.cloud import securitycenter

    """
    Retrieve an existing BigQuery export.
    Args:
        parent: Use any one of the following resource paths:
                 - organizations/{organization_id}
                 - folders/{folder_id}
                 - projects/{project_id}
        bigquery_export_id: Unique identifier that is used to identify the export.
    """

    client = securitycenter.SecurityCenterClient()

    request = securitycenter.GetBigQueryExportRequest()
    request.name = f"{parent}/bigQueryExports/{bigquery_export_id}"

    response = client.get_big_query_export(request)
    print(f"Retrieved the BigQuery export: {response.name}")


# [END securitycenter_get_bigquery_export]


# [START securitycenter_list_bigquery_export]
def list_bigquery_exports(parent: str):
    from google.cloud import securitycenter

    """
    List BigQuery exports in the given parent.
    Args:
         parent: The parent which owns the collection of BigQuery exports.
             Use any one of the following resource paths:
                 - organizations/{organization_id}
                 - folders/{folder_id}
                 - projects/{project_id}
    """

    client = securitycenter.SecurityCenterClient()

    request = securitycenter.ListBigQueryExportsRequest()
    request.parent = parent

    response = client.list_big_query_exports(request)

    print("Listing BigQuery exports:")
    for bigquery_export in response:
        print(bigquery_export.name)


# [END securitycenter_list_bigquery_export]


# [START securitycenter_update_bigquery_export]
def update_bigquery_export(parent: str, export_filter: str, bigquery_export_id: str):
    """
    Updates an existing BigQuery export.
    Args:
        parent: Use any one of the following resource paths:
                 - organizations/{organization_id}
                 - folders/{folder_id}
                 - projects/{project_id}
        export_filter: Expression that defines the filter to apply across create/update events of findings.
        bigquery_export_id: Unique identifier provided by the client.
        For more info, see:
        https://cloud.google.com/security-command-center/docs/how-to-analyze-findings-in-big-query#export_findings_from_to
    """
    from google.cloud import securitycenter
    from google.protobuf import field_mask_pb2

    client = securitycenter.SecurityCenterClient()

    # Set the new values for export configuration.
    bigquery_export = securitycenter.BigQueryExport()
    bigquery_export.name = f"{parent}/bigQueryExports/{bigquery_export_id}"
    bigquery_export.filter = export_filter

    # Field mask to only update the export filter.
    # Set the update mask to specify which properties should be updated.
    # If empty, all mutable fields will be updated.
    # For more info on constructing field mask path, see the proto or:
    # https://googleapis.dev/python/protobuf/latest/google/protobuf/field_mask_pb2.html
    field_mask = field_mask_pb2.FieldMask(paths=["filter"])

    request = securitycenter.UpdateBigQueryExportRequest()
    request.big_query_export = bigquery_export
    request.update_mask = field_mask

    response = client.update_big_query_export(request)

    if response.filter != export_filter:
        print("Failed to update BigQueryExport!")
        return
    print("BigQueryExport updated successfully!")


# [END securitycenter_update_bigquery_export]


# [START securitycenter_delete_bigquery_export]
def delete_bigquery_export(parent: str, bigquery_export_id: str):
    """
    Delete an existing BigQuery export.
    Args:
        parent: Use any one of the following resource paths:
                 - organizations/{organization_id}
                 - folders/{folder_id}
                 - projects/{project_id}
        bigquery_export_id: Unique identifier that is used to identify the export.
    """
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    request = securitycenter.DeleteBigQueryExportRequest()
    request.name = f"{parent}/bigQueryExports/{bigquery_export_id}"

    client.delete_big_query_export(request)
    print(f"BigQuery export request deleted successfully: {bigquery_export_id}")


# [END securitycenter_delete_bigquery_export]

#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets 
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa
from google.cloud import compute_v1


# <INGREDIENT set_usage_export_bucket>
def set_usage_export_bucket(
    project_id: str, bucket_name: str, report_name_prefix: str = ""
) -> None:
    """
    Set Compute Engine usage export bucket for the Cloud project.
    This sample presents how to interpret the default value for the
    report name prefix parameter.

    Args:
        project_id: project ID or project number of the project to update.
        bucket_name: Google Cloud Storage bucket used to store Compute Engine
            usage reports. An existing Google Cloud Storage bucket is required.
        report_name_prefix: Prefix of the usage report name which defaults to an empty string
            to showcase default values behaviour.
    """
    usage_export_location = compute_v1.UsageExportLocation()
    usage_export_location.bucket_name = bucket_name
    usage_export_location.report_name_prefix = report_name_prefix

    if not report_name_prefix:
        # Sending an empty value for report_name_prefix results in the
        # next usage report being generated with the default prefix value
        # "usage_gce". (ref: https://cloud.google.com/compute/docs/reference/rest/v1/projects/setUsageExportBucket)
        print(
            "Setting report_name_prefix to empty value causes the report "
            "to have the default prefix of `usage_gce`."
        )

    projects_client = compute_v1.ProjectsClient()
    operation = projects_client.set_usage_export_bucket(
        project=project_id, usage_export_location_resource=usage_export_location
    )

    wait_for_extended_operation(operation, "setting GCE usage bucket")
# </INGREDIENT>


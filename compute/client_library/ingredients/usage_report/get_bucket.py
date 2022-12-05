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


# <INGREDIENT get_usage_export_bucket>
def get_usage_export_bucket(project_id: str) -> compute_v1.UsageExportLocation:
    """
    Retrieve Compute Engine usage export bucket for the Cloud project.
    Replaces the empty value returned by the API with the default value used
    to generate report file names.

    Args:
        project_id: project ID or project number of the project to update.
    Returns:
        UsageExportLocation object describing the current usage export settings
        for project project_id.
    """
    projects_client = compute_v1.ProjectsClient()
    project_data = projects_client.get(project=project_id)

    uel = project_data.usage_export_location

    if not uel.bucket_name:
        # The usage reports are disabled.
        return uel

    if not uel.report_name_prefix:
        # Although the server sent the empty string value, the next usage report
        # generated with these settings still has the default prefix value
        # "usage_gce". (see https://cloud.google.com/compute/docs/reference/rest/v1/projects/get)
        print(
            "Report name prefix not set, replacing with default value of "
            "`usage_gce`."
        )
        uel.report_name_prefix = "usage_gce"
    return uel
# </INGREDIENT>


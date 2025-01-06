#  Copyright 2024 Google LLC
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
from google.cloud.compute_v1.services.resource_policies import pagers


# <INGREDIENT list_schedule_snapshots>
def snapshot_schedule_list(project_id: str, region: str) -> pagers.ListPager:
    """
    Lists snapshot schedules for a specified project and region.
    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the snapshot schedules are located.
    Returns:
        ListPager: A pager for iterating through the list of snapshot schedules.
    """
    client = compute_v1.ResourcePoliciesClient()

    request = compute_v1.ListResourcePoliciesRequest(
        project=project_id,
        region=region,
        filter='status = "READY"',  # Optional filter
    )

    schedules = client.list(request=request)
    return schedules


# </INGREDIENT>

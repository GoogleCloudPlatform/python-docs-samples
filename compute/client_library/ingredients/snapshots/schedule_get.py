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


# <INGREDIENT get_schedule_snapshots>
def snapshot_schedule_get(
    project_id: str, region: str, snapshot_schedule_name: str
) -> compute_v1.ResourcePolicy:
    """
    Retrieves a snapshot schedule for a specified project and region.
    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the snapshot schedule is located.
        snapshot_schedule_name (str): The name of the snapshot schedule.
    Returns:
        compute_v1.ResourcePolicy: The retrieved snapshot schedule.
    """
    client = compute_v1.ResourcePoliciesClient()
    schedule = client.get(
        project=project_id, region=region, resource_policy=snapshot_schedule_name
    )
    return schedule


# </INGREDIENT>

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

from google.cloud.compute_v1.services.zone_operations import pagers


# <INGREDIENT list_zone_operations>
def list_zone_operations(
    project_id: str, zone: str, filter: str = ""
) -> pagers.ListPager:
    """
    List all recent operations the happened in given zone in a project. Optionally filter those
    operations by providing a filter. More about using the filter can be found here:
    https://cloud.google.com/compute/docs/reference/rest/v1/zoneOperations/list
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        filter: filter string to be used for this listing operation.
    Returns:
        List of preemption operations in given zone.
    """
    operation_client = compute_v1.ZoneOperationsClient()
    request = compute_v1.ListZoneOperationsRequest()
    request.project = project_id
    request.zone = zone
    request.filter = filter

    return operation_client.list(request)
# </INGREDIENT>

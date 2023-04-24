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


# <INGREDIENT delete_route>
def delete_route(project_id: str, route_name: str) -> None:
    """
    Delete a route in project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        route_name: name of the route to delete.
    """

    route_client = compute_v1.RoutesClient()
    operation = route_client.delete(project=project_id, route=route_name)

    wait_for_extended_operation(operation, "route deletion")
# </INGREDIENT>

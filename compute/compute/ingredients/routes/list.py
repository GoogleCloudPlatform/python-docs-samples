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
from typing import Iterable

from google.cloud import compute_v1


# <INGREDIENT list_routes>
def list_routes(project_id: str, ) -> Iterable[compute_v1.Route]:
    """
    Lists routes in project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.

    Returns:
        An iterable collection of routes found in given project.
    """

    route_client = compute_v1.RoutesClient()
    return route_client.list(project=project_id)
# </INGREDIENT>

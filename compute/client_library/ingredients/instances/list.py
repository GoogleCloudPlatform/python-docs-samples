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
from __future__ import annotations

from collections.abc import Iterable

from google.cloud import compute_v1


# <INGREDIENT list_instances>
def list_instances(project_id: str, zone: str) -> Iterable[compute_v1.Instance]:
    """
    List all instances in the given zone in the specified project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
    Returns:
        An iterable collection of Instance objects.
    """
    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project_id, zone=zone)

    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")

    return instance_list
# </INGREDIENT>


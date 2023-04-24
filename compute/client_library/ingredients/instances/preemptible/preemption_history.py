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
import datetime
from typing import List, Tuple


# <INGREDIENT preemption_history>
def preemption_history(
    project_id: str, zone: str, instance_name: str = None
) -> List[Tuple[str, datetime.datetime]]:
    """
    Get a list of preemption operations from given zone in a project. Optionally limit
    the results to instance name.
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        instance_name: name of the virtual machine to look for.
    Returns:
        List of preemption operations in given zone.
    """
    if instance_name:
        filter = (
            f'operationType="compute.instances.preempted" '
            f"AND targetLink:instances/{instance_name}"
        )
    else:
        filter = 'operationType="compute.instances.preempted"'

    history = []

    for operation in list_zone_operations(project_id, zone, filter):
        this_instance_name = operation.target_link.rsplit("/", maxsplit=1)[1]
        if instance_name and this_instance_name == instance_name:
            # The filter used is not 100% accurate, it's `contains` not `equals`
            # So we need to check the name to make sure it's the one we want.
            moment = datetime.datetime.fromisoformat(operation.insert_time)
            history.append((instance_name, moment))

    return history
# </INGREDIENT>

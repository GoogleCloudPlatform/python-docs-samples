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
# flake8: noqa

# <REGION compute_instances_bulk_insert>
# <IMPORTS/>

# <INGREDIENT wait_for_extended_operation />

# <INGREDIENT get_instance_template />

# <INGREDIENT bulk_insert_instance />


def create_five_instances(project_id: str, zone: str, template_name: str,
                          name_pattern: str):
    """
    Create five instances of an instance template.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        template_name: name of the template that will be used to create new VMs.
        name_pattern: The string pattern used for the names of the VMs.
    """
    template = get_instance_template(project_id, template_name)
    instances = bulk_insert_instance(project_id, zone, template, 5, name_pattern)
    return instances
# </REGION compute_instances_bulk_insert>

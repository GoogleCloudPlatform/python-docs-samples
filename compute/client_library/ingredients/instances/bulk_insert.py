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
from __future__ import annotations

from collections.abc import Iterable
import uuid

from google.cloud import compute_v1


# <INGREDIENT bulk_insert_instance>
def bulk_insert_instance(project_id: str, zone: str, template: compute_v1.InstanceTemplate,
                         count: int, name_pattern: str, min_count: int | None = None,
                         labels: dict | None = None) -> Iterable[compute_v1.Instance]:
    """
    Create multiple VMs based on an Instance Template. The newly created instances will
    be returned as a list and will share a label with key `bulk_batch` and a random
    value.

    If the bulk insert operation fails and the requested number of instances can't be created,
    and more than min_count instances are created, then those instances can be found using
    the `bulk_batch` label with value attached to the raised exception in bulk_batch_id
    attribute. So, you can use the following filter: f"label.bulk_batch={err.bulk_batch_id}"
    when listing instances in a zone to get the instances that were successfully created.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        template: an Instance Template to be used for creation of the new VMs.
        name_pattern: The string pattern used for the names of the VMs. The pattern
            must contain one continuous sequence of placeholder hash characters (#)
            with each character corresponding to one digit of the generated instance
            name. Example: a name_pattern of inst-#### generates instance names such
            as inst-0001 and inst-0002. If existing instances in the same project and
            zone have names that match the name pattern then the generated instance
            numbers start after the biggest existing number. For example, if there
            exists an instance with name inst-0050, then instance names generated
            using the pattern inst-#### begin with inst-0051. The name pattern
            placeholder #...# can contain up to 18 characters.
        count: The maximum number of instances to create.
        min_count (optional): The minimum number of instances to create. If no min_count is
            specified then count is used as the default value. If min_count instances
            cannot be created, then no instances will be created and instances already
            created will be deleted.
        labels (optional): A dictionary with labels to be added to the new VMs.
    """
    bulk_insert_resource = compute_v1.BulkInsertInstanceResource()
    bulk_insert_resource.source_instance_template = template.self_link
    bulk_insert_resource.count = count
    bulk_insert_resource.min_count = min_count or count
    bulk_insert_resource.name_pattern = name_pattern

    if not labels:
        labels = {}

    labels['bulk_batch'] = uuid.uuid4().hex
    instance_prop = compute_v1.InstanceProperties()
    instance_prop.labels = labels
    bulk_insert_resource.instance_properties = instance_prop

    bulk_insert_request = compute_v1.BulkInsertInstanceRequest()
    bulk_insert_request.bulk_insert_instance_resource_resource = bulk_insert_resource
    bulk_insert_request.project = project_id
    bulk_insert_request.zone = zone

    client = compute_v1.InstancesClient()
    operation = client.bulk_insert(bulk_insert_request)

    try:
        wait_for_extended_operation(operation, "bulk instance creation")
    except Exception as err:
        err.bulk_batch_id = labels['bulk_batch']
        raise err

    list_req = compute_v1.ListInstancesRequest()
    list_req.project = project_id
    list_req.zone = zone
    list_req.filter = " AND ".join(f"labels.{key}:{value}" for key, value in labels.items())
    return client.list(list_req)
# </INGREDIENT>

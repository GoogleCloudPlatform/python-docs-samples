# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START functions_label_gce_instance]
import re

from google.cloud import compute_v1
from google.cloud.compute_v1.types import compute

instances_client = compute_v1.InstancesClient()


# CloudEvent function that labels newly-created GCE instances with the entity
# (person or service account) that created them.
#
# @param {object} cloudevent A CloudEvent containing the Cloud Audit Log entry.
# @param {object} cloudevent.data.protoPayload The Cloud Audit Log entry.
def label_gce_instance(cloudevent):
    # Extract parameters from the CloudEvent + Cloud Audit Log data
    payload = cloudevent.data.get('protoPayload')
    auth_info = payload.get('authenticationInfo', dict())
    creator = auth_info.get('principalEmail')

    # Get relevant VM instance details from the cloudevent's `subject` property
    # Example value:
    #   compute.googleapis.com/projects/<PROJECT>/zones/<ZONE>/instances/<INSTANCE>
    params = cloudevent['subject'].split('/')
    params_project = params[2]
    params_zone = params[4]
    params_instance = params[6]

    # Validate data
    if not creator or not params or len(params) != 7:
        raise ValueError('Invalid event structure')

    # Format the 'creator' parameter to match GCE label validation requirements
    creator = re.sub('\\W', '_', creator.lower())

    # Get the newly-created VM instance's label fingerprint
    # This is required by the Compute Engine API to prevent duplicate labels
    instance = instances_client.get(
        project=params_project,
        zone=params_zone,
        instance=params_instance
    )

    # Label the instance with its creator
    request_init = {
        'project': params_project,
        'zone': params_zone,
        'instance': params_instance
    }
    request_init['instances_set_labels_request_resource'] = \
        compute.InstancesSetLabelsRequest(
            label_fingerprint=instance.label_fingerprint,
            labels={'creator': creator}
        )
    request = compute.SetLabelsInstanceRequest(request_init)

    instances_client.set_labels(request)

    return
# [END functions_label_gce_instance]

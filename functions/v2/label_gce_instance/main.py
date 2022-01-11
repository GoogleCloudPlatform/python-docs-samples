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

from google.api_core.exceptions import GoogleAPIError
from google.cloud import compute_v1
from google.cloud.compute_v1.types import compute

instances_client = compute_v1.InstancesClient()


# CloudEvent function that labels newly-created GCE instances
# with the entity (user or service account) that created them.
#
# @param {object} cloudevent A CloudEvent containing the Cloud Audit Log entry.
# @param {object} cloudevent.data.protoPayload The Cloud Audit Log entry.
def label_gce_instance(cloudevent):
    # Extract parameters from the CloudEvent + Cloud Audit Log data
    payload = cloudevent.data.get('protoPayload', dict())
    auth_info = payload.get('authenticationInfo', dict())
    creator = auth_info.get('principalEmail')

    # Get relevant VM instance details from the cloudevent's `subject` property
    # Example value:
    #   compute.googleapis.com/projects/<PROJECT_ID>/zones/<ZONE_ID>/instances/<INSTANCE_NAME>
    instance_params = cloudevent['subject'].split('/')

    # Validate data
    if not creator or not instance_params or len(instance_params) != 7:
        # This is not something retries will fix, so don't throw an Exception
        # (Thrown exceptions trigger retries *if* you enable retries in GCF.)
        print('ERROR: Invalid `principalEmail` and/or CloudEvent `subject`.')
        return

    instance_project = instance_params[2]
    instance_zone = instance_params[4]
    instance_name = instance_params[6]

    # Format the 'creator' parameter to match GCE label validation requirements
    creator = re.sub('\\W', '_', creator.lower())

    # Get the newly-created VM instance's label fingerprint
    # This is required by the Compute Engine API to prevent duplicate labels
    instance = instances_client.get(
        project=instance_project,
        zone=instance_zone,
        instance=instance_name
    )

    # Construct API call to label the VM instance with its creator
    request_init = {
        'project': instance_project,
        'zone': instance_zone,
        'instance': instance_name
    }
    request_init['instances_set_labels_request_resource'] = \
        compute.InstancesSetLabelsRequest(
            label_fingerprint=instance.label_fingerprint,
            labels={'creator': creator}
        )
    request = compute.SetLabelsInstanceRequest(request_init)

    # Perform instance-labeling API call
    try:
        instances_client.set_labels_unary(request)
        print(f'Labelled VM instance {instance_name} with creator: {creator}')
    except GoogleAPIError as e:
        # Swallowing the exception means failed invocations WON'T be retried
        print('Label operation failed', e)

        # Uncomment the line below to retry failed invocations.
        # (You'll also have to enable retries in Cloud Functions itself.)
        # raise e

    return
# [END functions_label_gce_instance]

# Copyright 2018 Google LLC
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

# [START functions_start_instance_pubsub]
# [START functions_stop_instance_pubsub]
import base64
import json

import googleapiclient.discovery

_compute = googleapiclient.discovery.build('compute', 'v1')


# [END functions_stop_instance_pubsub]
# [END functions_start_instance_pubsub]
# [START functions_start_instance_pubsub]
def start_instance_pubsub(event, context):
    """Background Cloud Function that starts a Compute Engine instance.

    Expects a PubSub message with JSON-formatted event data containing the
    following attributes:
      project - the GCP project the instance belongs to.
      zone - the GCP zone the instance is located in.
      instance - the name of the instance.

    Args:
        data (dict): Cloud PubSub message event.
        context (google.cloud.functions.Context): Cloud PubSub event metadata.
    """
    if 'data' not in event:
        raise ValueError("PubSub message missing 'data' payload")

    payload = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    _validate_payload(payload)

    _compute.instances().start(
        project=payload['project'],
        zone=payload['zone'],
        instance=payload['instance']).execute()


# [END functions_start_instance_pubsub]
# [START functions_stop_instance_pubsub]
def stop_instance_pubsub(event, context):
    """Background Cloud Function that stops a Compute Engine instance.

    Expects a PubSub message with JSON-formatted event data containing the
    following attributes:
      project - the GCP project the instance belongs to.
      zone - the GCP zone the instance is located in.
      instance - the name of the instance.

    Args:
        data (dict): Cloud PubSub message event.
        context (google.cloud.functions.Context): Cloud PubSub event metadata.
    """
    if 'data' not in event:
        raise ValueError("PubSub message missing 'data' payload")

    payload = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    _validate_payload(payload)

    _compute.instances().stop(
        project=payload['project'],
        zone=payload['zone'],
        instance=payload['instance']).execute()


# [END functions_stop_instance_pubsub]
# [START functions_start_instance_pubsub]
# [START functions_stop_instance_pubsub]
def _validate_payload(payload):
    """Validates the specified payload contains the expected attributes.

    Args:
        payload (dict): a PubSub message payload.
    """
    if 'project' not in payload:
        raise ValueError("Attribute 'project' missing from payload")
    elif 'zone' not in payload:
        raise ValueError("Attribute 'zone' missing from payload")
    elif 'instance' not in payload:
        raise ValueError("Attribute 'instance' missing from payload")
# [END functions_start_instance_pubsub]
# [END functions_stop_instance_pubsub]

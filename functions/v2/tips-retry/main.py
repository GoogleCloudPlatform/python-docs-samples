# Copyright 2023 Google LLC
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


# [START functions_cloudevent_tips_retry]
import base64
import json

import functions_framework
from google.cloud import error_reporting


error_client = error_reporting.Client()


@functions_framework.cloud_event
def retry_or_not(cloud_event):
    """Cloud Event Function that demonstrates how to toggle retries.

    Args:
        cloud_event: The cloud event with a Pub/Sub data payload
    Returns:
        None; output is written to Stackdriver Logging
    """

    # The Pub/Sub event payload is passed as the CloudEvent's data payload.
    # See the documentation for more details:
    # https://cloud.google.com/eventarc/docs/cloudevents#pubsub
    encoded_pubsub_message = cloud_event.data["message"]["data"]

    # Retry based on a user-defined parameter
    try_again = json.loads(base64.b64decode(encoded_pubsub_message).decode())["retry"]

    try:
        raise RuntimeError("I failed you")
    except RuntimeError:
        error_client.report_exception()
        if try_again:
            raise  # Raise the exception and try again
        else:
            pass  # Swallow the exception and don't retry


# [END functions_cloudevent_tips_retry]

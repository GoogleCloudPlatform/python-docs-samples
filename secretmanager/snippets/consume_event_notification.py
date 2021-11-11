#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
"""
sample code for consuming an event notification in a cloud function.
"""

import base64


# [START secretmanager_consume_event_notification]
def consume_event_notification(event, unused_context):
    """
    consume_event_notification demonstrates how to consume and process a
    Pub/Sub notification from Secret Manager.
    Args:
          event (dict): Event payload.
          unused_context (google.cloud.functions.Context): Metadata for the event.
    """
    event_type = event["attributes"]["eventType"]
    secret_id = event["attributes"]["secretId"]
    secret_metadata = base64.b64decode(event["data"]).decode("utf-8")
    return f"Received {event_type} for {secret_id}. New metadata: {secret_metadata}"


# [END secretmanager_consume_event_notification]

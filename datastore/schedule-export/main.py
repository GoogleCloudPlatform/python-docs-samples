# Copyright 2021 Google LLC All Rights Reserved.
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
# limitations under the License.

import base64
import json
import os

from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache


class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


# The default cache (file_cache) is unavailable when using oauth2client >= 4.0.0 or google-auth,
# and it will log worrisome messages unless given another interface to use.
datastore = build("datastore", "v1", cache=MemoryCache())
project_id = os.environ.get("GCP_PROJECT")


def datastore_export(event, context):
    """Triggers a Datastore export from a Cloud Scheduler job.

    Args:
        event (dict): event[data] must contain a json object encoded in
            base-64. Cloud Scheduler encodes payloads in base-64 by default.
            Object must include a 'bucket' value and can include 'kinds'
            and 'namespaceIds' values.
        context (google.cloud.functions.Context): The Cloud Functions event
            metadata.
    """

    if "data" in event:
        # Triggered via Cloud Scheduler, decode the inner data field of the json payload.
        json_data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    else:
        # Otherwise, for instance if triggered via the Cloud Console on a Cloud Function, the event is the data.
        json_data = event

    bucket = json_data["bucket"]
    entity_filter = {}

    if "kinds" in json_data:
        entity_filter["kinds"] = json_data["kinds"]

    if "namespaceIds" in json_data:
        entity_filter["namespaceIds"] = json_data["namespaceIds"]

    request_body = {"outputUrlPrefix": bucket, "entityFilter": entity_filter}

    export_request = datastore.projects().export(
        projectId=project_id, body=request_body
    )
    response = export_request.execute()
    print(response)

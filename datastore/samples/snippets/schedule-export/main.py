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
# limitations under the License.

import base64
import json
import os

from google.cloud import datastore_admin_v1

project_id = os.environ.get("GCP_PROJECT")
client = datastore_admin_v1.DatastoreAdminClient()


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
    entity_filter = datastore_admin_v1.EntityFilter()

    if "kinds" in json_data:
        entity_filter.kinds = json_data["kinds"]

    if "namespaceIds" in json_data:
        entity_filter.namespace_ids = json_data["namespaceIds"]

    export_request = datastore_admin_v1.ExportEntitiesRequest(
        project_id=project_id, output_url_prefix=bucket, entity_filter=entity_filter
    )
    operation = client.export_entities(request=export_request)
    response = operation.result()
    print(response)

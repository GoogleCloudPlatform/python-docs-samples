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

# [START dialogflow_es_update_intent]

from google.cloud.dialogflow_v2 import IntentsClient
from google.protobuf import field_mask_pb2


def update_intent(project_id, intent_id, display_name):
    intents_client = IntentsClient()

    intent_name = intents_client.intent_path(project_id, intent_id)
    intent = intents_client.get_intent(request={"name": intent_name})

    intent.display_name = display_name
    update_mask = field_mask_pb2.FieldMask(paths=["display_name"])
    response = intents_client.update_intent(intent=intent, update_mask=update_mask)
    return response


# [END dialogflow_es_update_intent]

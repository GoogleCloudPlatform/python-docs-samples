# Copyright 2021, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# returns fullfillment response for dialogflow detect_intent call

# [START dialogflow_webhook]

# TODO: change the default Entry Point text to handleWebhook

def handleWebhook(request):

    req = request.get_json()

    responseText = ""
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "Default Welcome Intent":
        responseText = "Hello from a GCF Webhook"
    elif intent == "get-agent-name":
        responseText = "My name is Flowhook"
    else:
        responseText = f"There are no fulfillment responses defined for Intent {intent}"

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}

    return res


# [END dialogflow_webhook]

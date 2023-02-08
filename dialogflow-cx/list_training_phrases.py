# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START dialogflow_list_training_phrases]


def list_training_phrases(project_id, agent_id, intent_id, location):
    """Returns all training phrases for a specified intent."""

    from google.cloud import dialogflowcx

    # Create the intents client
    intent_client = dialogflowcx.IntentsClient()

    # Specify working intent
    intent_name = intent_client.intent_path(project_id, location, agent_id, intent_id)

    # Compose the get-intent request
    get_intent_request = dialogflowcx.GetIntentRequest(name=intent_name)

    intent = intent_client.get_intent(get_intent_request)

    # Iterate through the training phrases.
    for phrase in intent.training_phrases:
        print(phrase)

    return intent.training_phrases


# [END dialogflow_list_training_phrases]

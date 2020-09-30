#!/usr/bin/env python

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DialogFlow API Detect Intent Python sample with text inputs.

Examples:
  python detect_intent_texts.py -h
  python detect_intent_texts.py --agent AGENT \
  --session-id SESSION_ID \
  "hello" "book a meeting room" "Mountain View"
  python detect_intent_texts.py --agent AGENT \
  --session-id SESSION_ID \
  "tomorrow" "10 AM" "2 hours" "10 people" "A" "yes"
"""

import argparse
import uuid

from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session


# [START dialogflow_detect_intent_text]
def run_sample():
    # TODO(developer): Replace these values when running the function
    project_id = "YOUR-PROJECT-ID"
    location_id = "YOUR-LOCATION-ID"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "YOUR-AGENT-ID"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    session_id = uuid.uuid4()
    texts = ["Hello"]
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "en-us"

    detect_intent_texts(agent, session_id, texts, language_code)


def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = SessionsClient()
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")

    for text in texts:
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=language_code)
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")


# [END dialogflow_detect_intent_text]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--agent", help="Agent resource name.  Required.", required=True
    )
    parser.add_argument(
        "--session-id",
        help="Identifier of the DetectIntent session. " "Defaults to a random UUID.",
        default=str(uuid.uuid4()),
    )
    parser.add_argument(
        "--language-code",
        help='Language code of the query. Defaults to "en-US".',
        default="en-US",
    )
    parser.add_argument("texts", nargs="+", type=str, help="Text inputs.")

    args = parser.parse_args()

    detect_intent_texts(args.agent, args.session_id, args.texts, args.language_code)

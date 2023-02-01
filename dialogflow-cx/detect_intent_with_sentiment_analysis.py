#!/usr/bin/env python

# Copyright 2022 Google LLC
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

"""DialogFlow Detect Intent Python sample, text input and sentiment analysis."""


# [START dialogflow_cx_v3_detect_intent_sentiment_analysis_async]
import uuid

from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session


def run_sample():
    # TODO(developer): Update these values when running the function
    project_id = "YOUR-PROJECT-ID"
    location = "YOUR-LOCATION-ID"
    agent_id = "YOUR-AGENT-ID"
    text = "Perfect!"
    language_code = "en-us"

    detect_intent_with_sentiment_analysis(
        project_id,
        location,
        agent_id,
        text,
        language_code,
    )


def detect_intent_with_sentiment_analysis(
    project_id,
    location,
    agent_id,
    text,
    language_code,
):
    """Returns the result of detect intent with sentiment analysis"""

    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(uuid.uuid4())

    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )

    text_input = session.TextInput(text=text)
    query_input = session.QueryInput(text=text_input, language_code=language_code)
    query_params = session.QueryParameters(
        analyze_query_text_sentiment=True,
    )
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
        query_params=query_params,
    )

    response = session_client.detect_intent(request=request)
    score = response.query_result.sentiment_analysis_result.score
    print("Sentiment Score: {score}")
    return score


# [END dialogflow_cx_v3_detect_intent_sentiment_analysis_async]


if __name__ == "__main__":
    run_sample()

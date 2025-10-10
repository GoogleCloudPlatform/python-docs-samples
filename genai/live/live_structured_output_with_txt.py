# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Test file: https://storage.googleapis.com/generativeai-downloads/data/16000.wav
# Install helpers for converting files: pip install librosa soundfile

from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def generate_content() -> CalendarEvent:
    # [START googlegenaisdk_live_structured_output_with_txt]
    import os

    import google.auth.transport.requests
    import openai
    from google.auth import default
    from openai.types.chat import (ChatCompletionSystemMessageParam,
                                   ChatCompletionUserMessageParam)

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = "us-central1"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())
    # Note: the credential lives for 1 hour by default (https://cloud.google.com/docs/authentication/token-types#at-lifetime); after expiration, it must be refreshed.

    ##############################
    # Choose one of the following:
    ##############################

    # If you are calling a Gemini model, set the ENDPOINT_ID variable to use openapi.
    ENDPOINT_ID = "openapi"

    # If you are calling a self-deployed model from Model Garden, set the
    # ENDPOINT_ID variable and set the client's base URL to use your endpoint.
    # ENDPOINT_ID = "YOUR_ENDPOINT_ID"

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/{ENDPOINT_ID}",
        api_key=credentials.token,
    )

    completion = client.beta.chat.completions.parse(
        model="google/gemini-2.0-flash-001",
        messages=[
            ChatCompletionSystemMessageParam(
                role="system", content="Extract the event information."
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content="Alice and Bob are going to a science fair on Friday.",
            ),
        ],
        response_format=CalendarEvent,
    )

    response = completion.choices[0].message.parsed
    print(response)

    # System message: Extract the event information.
    # User message: Alice and Bob are going to a science fair on Friday.
    # Output message: name='science fair' date='Friday' participants=['Alice', 'Bob']
    # [END googlegenaisdk_live_structured_output_with_txt]
    return response


if __name__ == "__main__":
    generate_content()

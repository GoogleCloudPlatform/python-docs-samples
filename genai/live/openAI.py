import os

from pydantic import BaseModel
from openai import OpenAI

import openai

from google.auth import default
import google.auth.transport.requests

# TODO(developer): Update and un-comment below lines
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


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model="google/gemini-2.0-flash-001",
    # model="google/gemini-2.5-flash-preview-04-17",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    response_format=CalendarEvent,
)


print(completion.choices[0].message.parsed)

# Copyright 2024 Google LLC
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

# Disable linting on `Any` type annotations (needed for OpenAI kwargs and attributes).
# flake8: noqa ANN401

# [START generativeaionvertexai_credentials_refresher]
from typing import Any

import google.auth
import google.auth.transport.requests
import openai


class OpenAICredentialsRefresher:
    def __init__(self, **kwargs: Any) -> None:
        # Set a placeholder key here
        self.client = openai.OpenAI(**kwargs, api_key="PLACEHOLDER")
        self.creds, self.project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

    def __getattr__(self, name: str) -> Any:
        if not self.creds.valid:
            self.creds.refresh(google.auth.transport.requests.Request())

            if not self.creds.valid:
                raise RuntimeError("Unable to refresh auth")

            self.client.api_key = self.creds.token
        return getattr(self.client, name)


# [END generativeaionvertexai_credentials_refresher]
def generate_text(project_id: str, location: str = "us-central1") -> object:
    # [START generativeaionvertexai_credentials_refresher]

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"

    client = OpenAICredentialsRefresher(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
    )

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001",
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    )

    print(response)
    # [END generativeaionvertexai_credentials_refresher]

    return response

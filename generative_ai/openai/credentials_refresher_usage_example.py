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
import os

from credentials_refresher_class_example import OpenAICredentialsRefresher

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_text() -> object:
    # [START generativeaionvertexai_credentials_refresher_usage]

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    location = "us-central1"

    client = OpenAICredentialsRefresher(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
    )

    response = client.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    )

    print(response.choices[0].message.content)
    # Example response:
    # The sky is blue due to a phenomenon called **Rayleigh scattering**.
    # Sunlight is made up of all the colors of the rainbow.
    # When sunlight enters the Earth's atmosphere, it collides with ...

    # [END generativeaionvertexai_credentials_refresher_usage]
    return response


if __name__ == "__main__":
    generate_text()

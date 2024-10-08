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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_text() -> object:
    # [START generativeaionvertexai_gemini_chat_completions_streaming_image]
    import vertexai
    import openai

    from google.auth import default, transport

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    location = "us-central1"

    vertexai.init(project=PROJECT_ID, location=location)

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_request = transport.requests.Request()
    credentials.refresh(auth_request)

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the following image:"},
                    {
                        "type": "image_url",
                        "image_url": "gs://cloud-samples-data/generative-ai/image/scones.jpg",
                    },
                ],
            }
        ],
        stream=True,
    )
    for chunk in response:
        print(chunk.choices[0].delta.content)
    # Example response:
    # Here's a description of the image:
    # High-angle, close-up view of a rustic scene featuring several blueberry
    # scones arranged on a piece of parchment paper...

    # [END generativeaionvertexai_gemini_chat_completions_streaming_image]
    return response


if __name__ == "__main__":
    generate_text()

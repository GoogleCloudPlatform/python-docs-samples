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


def generate_text(
    project_id: str,
    location: str = "us-central1",
    model_id: str = "gemma-2-9b-it",
    endpoint_id: str = "YOUR_ENDPOINT_ID",
) -> object:
    # [START generativeaionvertexai_gemini_chat_completions_non_streaming_self_deployed]
    from google.auth import default
    import google.auth.transport.requests

    import openai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"
    # model_id = "gemma-2-9b-it"
    # endpoint_id = "YOUR_ENDPOINT_ID"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/{endpoint_id}",
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    )
    print(response)

    # [END generativeaionvertexai_gemini_chat_completions_non_streaming_self_deployed]

    return response

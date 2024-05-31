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


def example(project_id: str, location: str = "us-central1") -> str:
    """Streaming Chat Example with a Large Language Model."""
    # [START generativeaionvertexai_gemini_chat_completion_streaming]
    import vertexai
    import openai

    from google.auth import default, transport

    # TODO(developer): update project_id & location
    vertexai.init(project=project_id, location=location)

    # Programmatically get an access token
    creds, _ = default()
    auth_req = transport.requests.Request()
    creds.refresh(auth_req)

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{location}/endpoints/openapi",
        api_key=creds.token,
    )

    responses = client.chat.completions.create(
        model="google/gemini-1.5-flash-001",
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
        stream=True,
    )
    for chunk in responses:
        print(chunk)
    # [END generativeaionvertexai_gemini_chat_completion_streaming]
    return f"{chunk.model}:{chunk.choices[0].delta.content}"

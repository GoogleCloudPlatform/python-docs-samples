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

# [START aiplatform_claude_3_streaming]
# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
# pip3 install -U 'anthropic[vertex]'

from anthropic import AnthropicVertex


def generate_text_streaming(project_id: str, region: str) -> str:
    client = AnthropicVertex(region=region, project_id=project_id)
    result = []

    with client.messages.stream(
        model="claude-3-sonnet@20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Send me a recipe for banana bread.",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    return "".join(result)


# [END aiplatform_claude_3_streaming]


if __name__ == "__main__":
    generate_text_streaming()

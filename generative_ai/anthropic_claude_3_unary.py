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

# [START aiplatform_claude_3_unary]
# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
# pip3 install -U 'anthropic[vertex]'

from anthropic import AnthropicVertex


def generate_text(project_id: str, region: str) -> object:
    client = AnthropicVertex(region=region, project_id=project_id)
    message = client.messages.create(
        model="claude-3-sonnet@20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Send me a recipe for banana bread.",
            }
        ],
    )
    print(message.model_dump_json(indent=2))
    return message


# [END aiplatform_claude_3_unary]


if __name__ == "__main__":
    generate_text()

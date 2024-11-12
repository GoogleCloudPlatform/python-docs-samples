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


def generate_text_streaming() -> str:
    # [START generativeaionvertexai_claude_3_streaming]
    # TODO(developer): Vertex AI SDK - uncomment below & run
    # pip3 install --upgrade --user google-cloud-aiplatform
    # gcloud auth application-default login
    # pip3 install -U 'anthropic[vertex]'

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    from anthropic import AnthropicVertex

    client = AnthropicVertex(project_id=PROJECT_ID, region="us-east5")
    result = []

    with client.messages.stream(
        model="claude-3-5-sonnet-v2@20241022",
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

    # Example response:
    # Here's a simple recipe for delicious banana bread:
    # Ingredients:
    # - 2-3 ripe bananas, mashed
    # - 1/3 cup melted butter
    # ...
    # ...
    # 8. Bake for 50-60 minutes, or until a toothpick inserted into the center comes out clean.
    # 9. Let cool in the pan for a few minutes, then remove and cool completely on a wire rack.

    # [END generativeaionvertexai_claude_3_streaming]
    return "".join(result)


if __name__ == "__main__":
    generate_text_streaming()

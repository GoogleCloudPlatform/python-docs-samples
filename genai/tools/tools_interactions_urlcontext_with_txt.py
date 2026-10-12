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


def generate_content() -> str:
    # [START googlegenaisdk_interactions_tools_urlcontext_with_txt]
    from google import genai

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    # TODO(developer): Here put your URLs
    url1 = "https://cloud.google.com/vertex-ai/docs/generative-ai/start"
    url2 = "https://cloud.google.com/docs/overview"

    interaction = client.interactions.create(
        model=model_id,
        input=f"Compare the content, purpose, and audiences of {url1} and {url2}.",
        tools=[{"type": "url_context"}],
    )

    print(interaction.output_text)

    # Inspect URL context metadata from interaction steps
    for step in interaction.steps:
        if step.type == "url_context_result":
            print(step.result)

    # [END googlegenaisdk_interactions_tools_urlcontext_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()

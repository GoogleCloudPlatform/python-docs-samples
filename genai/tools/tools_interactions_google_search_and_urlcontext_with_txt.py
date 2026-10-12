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
    # [START googlegenaisdk_interactions_tools_google_search_and_urlcontext_with_txt]
    from google import genai

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    tools = [
        {"type": "url_context"},
        {"type": "google_search"},
    ]

    # TODO(developer): Here put your URLs!
    url = "https://www.google.com/search?q=events+in+New+York"

    interaction = client.interactions.create(
        model=model_id,
        input=f"Give me three day events schedule based on {url}. Also let me know what needs to taken care of considering weather and commute.",
        tools=tools,
    )

    print(interaction.output_text)

    # Inspect URL context results from interaction steps
    for step in interaction.steps:
        if step.type == "url_context_result":
            print(step.result)

    # [END googlegenaisdk_interactions_tools_google_search_and_urlcontext_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()

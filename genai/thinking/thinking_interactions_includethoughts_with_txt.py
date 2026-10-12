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
    # [START googlegenaisdk_interactions_thinking_includethoughts_with_txt]
    from google import genai

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.1-pro-preview",
        input="solve x^2 + 4x + 4 = 0",
        generation_config={
            "thinking_summaries": "auto",
        },
    )

    print(interaction.output_text)

    # Inspect thoughts step in interaction
    for step in interaction.steps:
        if step.type == "thought":
            print("Thought:")
            print(step.summary)

    # [END googlegenaisdk_interactions_thinking_includethoughts_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()

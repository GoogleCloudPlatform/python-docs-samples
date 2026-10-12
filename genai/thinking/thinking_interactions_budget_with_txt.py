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
    # [START googlegenaisdk_interactions_thinking_budget_with_txt]
    from google import genai

    client = genai.Client()

    # The Interactions API controls thinking depth via thinking_level ("minimal", "low", "medium", "high")
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="solve x^2 + 4x + 4 = 0",
        generation_config={
            "thinking_level": "medium",
        },
    )

    print(interaction.output_text)

    # Thinking thoughts token count from usage
    if interaction.usage and interaction.usage.modality_tokens:
        for item in interaction.usage.modality_tokens:
            if item.modality == "thought":
                print(f"Thoughts tokens: {item.token_count}")

    if interaction.usage:
        print(f"Total tokens: {interaction.usage.total_tokens}")

    # [END googlegenaisdk_interactions_thinking_budget_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()

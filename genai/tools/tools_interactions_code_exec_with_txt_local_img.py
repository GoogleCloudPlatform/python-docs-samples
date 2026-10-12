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

from google.genai._gaos.types.interactions import Interaction


def generate_content() -> Interaction:
    # [START googlegenaisdk_interactions_tools_code_exec_with_txt_local_img]
    import base64
    from google import genai

    client = genai.Client()

    prompt = """
    Run a simulation of the Monty Hall Problem with 1,000 trials.
    Here's how this works as a reminder. In the Monty Hall Problem, you're on a game
    show with three doors. Behind one is a car, and behind the others are goats. You
    pick a door. The host, who knows what's behind the doors, opens a different door
    to reveal a goat. Should you switch to the remaining unopened door?
    The answer has always been a little difficult for me to understand when people
    solve it with math - so please run a simulation with Python to show me what the
    best strategy is.
    Thank you!
    """

    with open("test_data/640px-Monty_open_door.svg.png", "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode("utf-8")

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {"type": "image", "data": b64_image, "mime_type": "image/png"},
            prompt,
        ],
        tools=[{"type": "code_execution"}],
    )

    for step in interaction.steps:
        if step.type == "code_execution_call":
            print("# Code:")
            print(step.arguments.code)
        elif step.type == "code_execution_result":
            print("# Outcome:")
            print(step.result)

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_tools_code_exec_with_txt_local_img]
    return interaction


if __name__ == "__main__":
    generate_content()

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

from google.genai.types import GenerateContentResponse


def generate_content() -> GenerateContentResponse:
    # [START googlegenaisdk_tools_code_exec_with_txt_local_img]
    from PIL import Image
    from google import genai
    from google.genai.types import (
        GenerateContentConfig,
        HttpOptions,
        Tool,
        ToolCodeExecution,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    code_execution_tool = Tool(code_execution=ToolCodeExecution())

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

    # Image source: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Monty_open_door.svg/640px-Monty_open_door.svg.png
    with open("test_data/640px-Monty_open_door.svg.png", "rb") as image_file:
        image_data = Image.open(image_file)

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=[image_data, prompt],
            config=GenerateContentConfig(
                tools=[code_execution_tool],
                temperature=0,
            ),
        )

    print("# Code:")
    for part in response.candidates[0].content.parts:
        if part.executable_code:
            print(part.executable_code)

    print("# Outcome:")
    for part in response.candidates[0].content.parts:
        if part.code_execution_result:
            print(part.code_execution_result)

    # Example response:
    # # Code:
    # code='\nimport random\n\ndef monty_hall_simulation(num_trials):\n
    # """Simulates the Monty Hall problem and returns the win rates for switching and not switching."""\n\n
    # wins_switching = 0\n    wins_not_switching = 0\n\n    for _ in range(num_trials):\n        # 1. Set up the game:\n
    #   - Randomly place the car behind one of the three doors.\n        car_door = random.randint(0, 2)\n
    # ...
    # # Outcome:
    # outcome=<Outcome.OUTCOME_OK: 'OUTCOME_OK'> output='Win percentage when switching: 65.90%\nWin percentage when not switching: 34.10%\n'
    # [END googlegenaisdk_tools_code_exec_with_txt_local_img]
    return response


if __name__ == "__main__":
    generate_content()

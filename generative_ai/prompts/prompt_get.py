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

from vertexai.preview.prompts import Prompt

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_prompt() -> Prompt:
    """Retrieves a prompt that has been saved to the online resource"""

    # [START generativeaionvertexai_prompt_template_load_or_retrieve_prompt]
    import vertexai
    from vertexai.preview.prompts import Prompt
    from vertexai.preview import prompts

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Create local Prompt
    prompt = Prompt(
        prompt_name="meteorologist",
        prompt_data="How should I dress for weather in August?",
        model_name="gemini-2.0-flash-001",
        system_instruction="You are a meteorologist. Answer in a short sentence.",

    )
    # Save Prompt to online resource.
    prompt1 = prompts.create_version(prompt=prompt)
    prompt_id = prompt1.prompt_id

    # Get prompt
    get_prompt = prompts.get(prompt_id=prompt_id)

    print(get_prompt)

    # Example response
    # How should I dress for weather in August?
    # [END generativeaionvertexai_prompt_template_load_or_retrieve_prompt]
    return get_prompt


if __name__ == "__main__":
    get_prompt()

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


# [START aiplatform_genai_prompt_template_create]

import os

import agentplatform
from agentplatform.types import Prompt

from google import genai


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def prompt_create() -> None:
    agent_client = agentplatform.Client(project=PROJECT_ID, location=LOCATION_ID)

    system_part = genai.types.Part(text="You are a knowledgeable local tour guide.")

    user_part = genai.types.Part(
        text=("Write a short, exciting welcome message for a tourist"
              " named {name} visiting {city}. Highlight one famous local food.")
    )

    system_content = genai.types.Content(
        role="system",
        parts=[system_part]
    )

    user_content = genai.types.Content(
        role="user",
        parts=[user_part]
    )

    variables = {
        "name": genai.types.Part(text="Roberto"),
        "city": genai.types.Part(text="Tijuana")
    }

    prompt_data_payload = agentplatform.types.PromptData(
        model=GEMINI_MODEL,
        contents=[user_content],
        system_instruction=system_content,
        variables=[variables]
    )

    prompt_config = agentplatform.types.Prompt(
        prompt_data=prompt_data_payload
    )

    managed_prompt = agent_client.prompts.create(
        prompt=prompt_config
    )

    genai_client = genai.Client(
        enterprise=True,
        project=PROJECT_ID,
        location=LOCATION_ID
    )

    assembled_contents = managed_prompt.assemble_contents()

    response = genai_client.models.generate_content(
        model=managed_prompt.prompt_data.model,
        contents=assembled_contents
    )

    print(response.text)
    return response


if __name__ == "__main__":
    prompt_create()

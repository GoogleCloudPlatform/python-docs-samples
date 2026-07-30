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

from google import genai


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def prompt_create_2() -> None:
    agent_client = agentplatform.Client(project=PROJECT_ID, location=LOCATION_ID)

    system_part = genai.types.Part(text="You are a knowledgeable local tour guide.")

    user_part = genai.types.Part(
        text="Write a short, exciting welcome message for a tourist named {name} visiting {city}. Highlight one famous local food."
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
"""
def prompt_create() -> genai.types.Prompt:

    client = agentplatform.Client(project=PROJECT_ID, location=LOCATION_ID)

    # Create local Prompt
    agentplatform.types.Prompt
    local_prompt = client.prompts.create(
        prompt_name="movie-critic",
        prompt_data="Compare the movies {movie1} and {movie2}.",
        variables=[
            {"movie1": "The Lion King", "movie2": "Frozen"},
            {"movie1": "Inception", "movie2": "Interstellar"},
        ],
        model_name=GEMINI_MODEL,
        system_instruction="You are a movie critic. Answer in a short sentence.",
        # generation_config=GenerationConfig, # Optional,
        # safety_settings=SafetySetting, # Optional,
    )

    # Generate content using the assembled prompt for each variable set.
    for i in range(len(local_prompt.variables)):
        response = local_prompt.generate_content(
            contents=local_prompt.assemble_contents(**local_prompt.variables[i])
        )
        print(response)

    # Save a version
    prompt1 = prompts.create_version(prompt=local_prompt)

    print(prompt1)

    # Example response
    # Assembled prompt replacing: 1 instances of variable movie1, 1 instances of variable movie2
    # Assembled prompt replacing: 1 instances of variable movie1, 1 instances of variable movie2
    # Created prompt resource with id 12345678910.....

    # [END generativeaionvertexai_prompt_template_create_generate_save]
    return prompt1
"""

if __name__ == "__main__":
    prompt_create_2()

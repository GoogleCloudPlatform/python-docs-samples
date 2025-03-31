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


def prompt_create() -> Prompt:
    """Create a local prompt, generates content and saves prompt"""

    # [START generativeaionvertexai_prompt_template_create_generate_save]
    import vertexai
    from vertexai.preview import prompts
    from vertexai.preview.prompts import Prompt

    # from vertexai.generative_models import GenerationConfig, SafetySetting # Optional

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Create local Prompt
    local_prompt = Prompt(
        prompt_name="movie-critic",
        prompt_data="Compare the movies {movie1} and {movie2}.",
        variables=[
            {"movie1": "The Lion King", "movie2": "Frozen"},
            {"movie1": "Inception", "movie2": "Interstellar"},
        ],
        model_name="gemini-2.0-flash-001",
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


if __name__ == "__main__":
    prompt_create()

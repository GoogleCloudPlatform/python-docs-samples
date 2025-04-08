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

from vertexai.generative_models import GenerationResponse


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def prompt_template_example() -> list[GenerationResponse]:
    """Build a parameterized prompt template to generate content with multiple variable sets"""

    # [START generativeaionvertexai_prompt_template]
    import vertexai
    from vertexai.preview.prompts import Prompt

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    variables = [
        {"animal": "Eagles", "activity": "eat berries"},
        {"animal": "Coyotes", "activity": "jump"},
        {"animal": "Squirrels", "activity": "fly"}
    ]

    # define prompt template
    prompt = Prompt(
        prompt_data="Do {animal} {activity}?",
        model_name="gemini-2.0-flash-001",
        variables=variables,
        system_instruction="You are a helpful zoologist"
        # generation_config=generation_config, # Optional
        # safety_settings=safety_settings, # Optional
    )

    # Generates content using the assembled prompt.
    responses = []
    for variable_set in prompt.variables:
        response = prompt.generate_content(
            contents=prompt.assemble_contents(**variable_set)
        )
        responses.append(response)

    for response in responses:
        print(response.text, end="")

    # Example response
        # Assembled prompt replacing: 1 instances of variable animal, 1 instances of variable activity
        # Eagles are primarily carnivorous.  While they might *accidentally* ingest a berry......
    # [END generativeaionvertexai_prompt_template]
    return responses


if __name__ == "__main__":
    prompt_template_example()

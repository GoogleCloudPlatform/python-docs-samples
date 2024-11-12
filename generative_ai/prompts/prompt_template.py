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


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def prompt_template() -> str:
    """Create prompt template"""

    # [START generativeaionvertexai_prompt_template]
    import vertexai
    from vertexai.preview.prompts import Prompt

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    variables = [
        {
            "animal": ["""Eagles, Coyotes, Squirrels"""],
            "activity": ["""eat berries, jump, fly"""],
        },
    ]
    prompt = Prompt(
        prompt_data=["Do {animal}{activity}?"],  # Includes placeholders for vars
        model_name="gemini-1.5-flash-002",  # Model in use
        variables=variables,  # Lists variables defined above
        system_instruction=["You are a helpful zoolgist"]
        # generation_config=generation_config, # Optional
        # safety_settings=safety_settings, # Optional
    )
    # Generates content using the assembled prompt.
    responses = prompt.generate_content(
        contents=prompt.assemble_contents(**prompt.variables[0]),
        stream=True,
    )

    for response in responses:
        print(response.text, end="")

    # [END generativeaionvertexai_prompt_template]
    return responses


if __name__ == "__main__":
    prompt_template()

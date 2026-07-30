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


def list_prompt_version() -> list:
    """Displays a specific prompt version from the versions metadata list."""

    # [START generativeaionvertexai_prompt_list_prompt_version]
    import vertexai
    from vertexai.preview.prompts import Prompt
    from vertexai.preview import prompts

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Create local Prompt
    prompt = Prompt(
        prompt_name="zoologist",
        prompt_data="Which animal is the fastest on earth?",
        model_name="gemini-2.0-flash-001",
        system_instruction="You are a zoologist. Answer in a short sentence.",
    )
    # Save Prompt to online resource.
    prompt1 = prompts.create_version(prompt=prompt)
    prompt_id = prompt1.prompt_id

    # Get prompt a prompt from list
    prompt_versions_metadata = prompts.list_versions(prompt_id=prompt_id)

    # Get a specific prompt version from the versions metadata list
    prompt1 = prompts.get(
        prompt_id=prompt_versions_metadata[0].prompt_id,
        version_id=prompt_versions_metadata[0].version_id,
    )

    print(prompt1)
    # Example response:
    # Which animal is the fastest on earth?
    # [END generativeaionvertexai_prompt_list_prompt_version]
    return prompt_versions_metadata


if __name__ == "__main__":
    list_prompt_version()

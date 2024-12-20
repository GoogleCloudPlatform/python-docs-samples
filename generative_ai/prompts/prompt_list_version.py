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
MY_PROMPT = os.getenv("MY_PROMPT")


def list_prompt_version() -> list:
    """Displays a specific prompt version from the versions metadata list."""

    # [START generativeaionvertexai_prompt_list_prompt_version]
    import vertexai
    from vertexai.preview import prompts

    # TODO(developer): Update and un-comment below line
    # prompt_id = "your-prompt"

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Get prompt a prompt from list

    prompt_versions_metadata = prompts.list_versions(prompt_id=MY_PROMPT)

    # Get a specific prompt version from the versions metadata list
    prompt1 = prompts.get(
        prompt_id=prompt_versions_metadata[1].prompt_id,
        version_id=prompt_versions_metadata[1].version_id
    )

    print(prompt1)
    # Example response:
    # Give me a suggestion for an action packaged thriller.
    # [END generativeaionvertexai_prompt_list_prompt_version]
    return prompt1


if __name__ == "__main__":
    list_prompt_version()

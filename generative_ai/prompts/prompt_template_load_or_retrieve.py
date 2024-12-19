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


def load_prompt_generate() -> str:
    """Loads or retreives a prompt that has been saved to the online resource"""

    # [START generativeaionvertexai_prompt_template_load_or_retreive_prompt]
    import vertexai
    from vertexai.preview import prompts

    # TODO(developer): Update and un-comment below line
    # prompt_id = "your-prompt"

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Get prompt
    get_prompt = prompts.get(prompt_id="3524045267940671488")

    print(get_prompt)

    # Example response
    # Compare the movies {movie1} and {movie2}

    # [END generativeaionvertexai_prompt_template_load_or_retreive_prompt]
    return get_prompt


if __name__ == "__main__":
    load_prompt_generate()

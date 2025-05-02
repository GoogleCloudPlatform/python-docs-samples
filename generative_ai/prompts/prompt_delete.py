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


def delete_prompt() -> None:
    """Deletes specified prompt."""

    # [START generativeaionvertexai_prompt_delete]
    import vertexai
    from vertexai.preview.prompts import Prompt
    from vertexai.preview import prompts

    # Initialize vertexai
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Create local Prompt
    prompt = Prompt(
        prompt_name="movie-critic",
        prompt_data="Compare the movies {movie1} and {movie2}.",
        variables=[
            {"movie1": "The Lion King", "movie2": "Frozen"},
            {"movie1": "Inception", "movie2": "Interstellar"},
        ],
        model_name="gemini-2.0-flash-001",
        system_instruction="You are a movie critic. Answer in a short sentence.",

    )
    # Save a version
    prompt1 = prompts.create_version(prompt=prompt)
    prompt_id = prompt1.prompt_id

    # Delete prompt
    prompts.delete(prompt_id=prompt_id)
    print(f"Deleted prompt with ID: {prompt_id}")

    # Example response:
    # Deleted prompt resource with id 12345678910
    # [END generativeaionvertexai_prompt_delete]


if __name__ == "__main__":
    delete_prompt()

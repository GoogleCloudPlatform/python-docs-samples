# # Copyright 2024 Google LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #    https://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# import os
#
# from vertexai.preview.prompts import Prompt
#
# PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
#
#
# def restore_prompt_version() -> Prompt:
#     """Restores specified version for specified prompt."""
#
#     # [START generativeaionvertexai_prompt_restore_version]
#     import vertexai
#     from vertexai.preview import prompts
#
#     # Initialize vertexai
#     vertexai.init(project=PROJECT_ID, location="us-central1")
#
#     # Create local Prompt
#     prompt = Prompt(
#         prompt_name="zoologist",
#         prompt_data="Which animal is the fastest on earth?",
#         model_name="gemini-2.0-flash-001",
#         system_instruction="You are a zoologist. Answer in a short sentence.",
#     )
#     # Save Prompt to online resource.
#     prompt1 = prompts.create_version(prompt=prompt)
#     prompt_id = prompt1.prompt_id
#
#     # Restore to prompt version id 1 (original)
#     prompt_version_metadata = prompts.restore_version(prompt_id=prompt_id, version_id="1")
#
#     # Fetch the newly restored latest version of the prompt
#     prompt1 = prompts.get(prompt_id=prompt_version_metadata.prompt_id)
#
#     # Example response:
#     # Restored prompt version 1 under prompt id 12345678910 as version number 2
#     # [END generativeaionvertexai_prompt_restore_version]
#     return prompt1
#
#
# if __name__ == "__main__":
#     restore_prompt_version()

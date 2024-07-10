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


def generate_from_text_input(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_generate_from_text_input]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    response = model.generate_content(
        "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_generate_from_text_input]

    return response.text

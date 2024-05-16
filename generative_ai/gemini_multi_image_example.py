# Copyright 2023 Google LLC
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


def generate_text_multimodal(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_single_turn_multi_image]
    import vertexai

    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    # Load images from Cloud Storage URI
    image_file1 = Part.from_uri(
        "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png",
        mime_type="image/png",
    )
    image_file2 = Part.from_uri(
        "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark2.png",
        mime_type="image/png",
    )
    image_file3 = Part.from_uri(
        "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark3.png",
        mime_type="image/png",
    )

    model = GenerativeModel(model_name="gemini-1.0-pro-vision-001")
    response = model.generate_content(
        [
            image_file1,
            "city: Rome, Landmark: the Colosseum",
            image_file2,
            "city: Beijing, Landmark: Forbidden City",
            image_file3,
        ]
    )
    print(response.text)

    # [END generativeaionvertexai_gemini_single_turn_multi_image]
    return response.text

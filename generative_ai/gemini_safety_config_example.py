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

from vertexai.generative_models import Part


def generate_text(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_safety_settings]
    import vertexai

    from vertexai import generative_models

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = generative_models.GenerativeModel(model_name="gemini-1.0-pro-vision-001")

    # Generation config
    generation_config = generative_models.GenerationConfig(
        max_output_tokens=2048, temperature=0.4, top_p=1, top_k=32
    )

    # Safety config
    safety_config = [
        generative_models.SafetySetting(
            category=generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        generative_models.SafetySetting(
            category=generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]

    image_file = Part.from_uri(
        "gs://cloud-samples-data/generative-ai/image/scones.jpg", "image/jpeg"
    )

    # Generate content
    responses = model.generate_content(
        [image_file, "What is in this image?"],
        generation_config=generation_config,
        safety_settings=safety_config,
        stream=True,
    )

    text_responses = []
    for response in responses:
        print(response.text)
        text_responses.append(response.text)
    # [END generativeaionvertexai_gemini_safety_settings]

    return "".join(text_responses)

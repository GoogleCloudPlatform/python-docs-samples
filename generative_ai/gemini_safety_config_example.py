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

import vertexai

# [START aiplatform_gemini_safety_settings]
from vertexai.preview import generative_models


def generate_text(project_id: str, location: str, image: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = generative_models.GenerativeModel("gemini-pro-vision")

    # Generation config
    config = {"max_output_tokens": 2048, "temperature": 0.4, "top_p": 1, "top_k": 32}

    # Safety config
    safety_config = {
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    # Generate content
    responses = model.generate_content(
        [image, "Add your prompt here"],
        generation_config=config,
        stream=True,
        safety_settings=safety_config,
    )

    text_responses = []
    for response in responses:
        print(response.text)
        text_responses.append(response.text)
    return "".join(text_responses)


# [END aiplatform_gemini_safety_settings]


if __name__ == "__main__":
    import os
    import base64

    file_name = "scones.jpg"
    if os.path(file_name):
        base64_image_data = base64.b64encode(open(file_name, "rb").read()).decode(
            "utf-8"
        )
        image = generative_models.Part.from_data(
            data=base64.b64decode(base64_image_data), mime_type="image/png"
        )
        generate_text(image)

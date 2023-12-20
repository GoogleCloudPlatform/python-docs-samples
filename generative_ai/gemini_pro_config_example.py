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

# [START aiplatform_gemini_pro_config_image_example_parent]
import base64

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


# [START aiplatform_gemini_pro_config_image_example]
def generate_text(project_id: str, location: str) -> None:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel("gemini-pro-vision")

    # Load example image from local storage
    encoded_image = base64.b64encode(open("scones.jpg", "rb").read()).decode("utf-8")
    image_content = Part.from_data(
        data=base64.b64decode(encoded_image), mime_type="image/jpeg"
    )

    # Generation Config
    config = {"max_output_tokens": 2048, "temperature": 0.4, "top_p": 1, "top_k": 32}

    # Generate text
    response = model.generate_content(
        [image_content, "what is in this image"], generation_config=config
    )
    print(response.text)
    return response.text


# [END aiplatform_gemini_pro_config_image_example]
# [END aiplatform_gemini_pro_config_image_example_parent]

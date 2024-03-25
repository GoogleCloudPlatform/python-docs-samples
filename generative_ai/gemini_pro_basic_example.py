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

# [START generativeaionvertexai_gemini_pro_example]
import vertexai
from vertexai.generative_models import GenerativeModel, Part


def generate_text(project_id: str, location: str) -> None:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel(model_name="gemini-pro-vision")

    # Load example image
    image_url = "gs://generativeai-downloads/images/scones.jpg"
    image_content = Part.from_uri(image_url, "image/jpeg")

    # Query the model
    response = model.generate_content([image_content, "what is this image?"])
    print(response)

    return response.text


# [END generativeaionvertexai_gemini_pro_example]

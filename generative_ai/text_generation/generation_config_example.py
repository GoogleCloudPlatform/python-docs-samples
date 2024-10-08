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


def generate_text() -> None:
    # [START generativeaionvertexai_gemini_pro_config_example]
    import base64
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    # Load example image from local storage
    encoded_image = base64.b64encode(open("scones.jpg", "rb").read()).decode("utf-8")
    image_content = Part.from_data(
        data=base64.b64decode(encoded_image), mime_type="image/jpeg"
    )

    # Generation Config
    config = GenerationConfig(
        max_output_tokens=2048, temperature=0.4, top_p=1, top_k=32
    )

    # Generate text
    response = model.generate_content(
        [image_content, "what is this image?"], generation_config=config
    )
    print(response.text)
    # Example response:
    # That's a lovely overhead shot of a rustic still life featuring blueberry scones.
    # Here's a breakdown of what's in the image:
    # * **Blueberry Scones:** Several freshly baked blueberry scones are arranged on
    # a piece of parchment paper. They appear to be homemade and slightly crumbly.
    # ...

    # [END generativeaionvertexai_gemini_pro_config_example]
    return response.text


if __name__ == "__main__":
    generate_text()

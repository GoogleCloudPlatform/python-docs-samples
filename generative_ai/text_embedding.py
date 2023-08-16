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

# [START aiplatform_sdk_text_embedding]
import vertexai
from vertexai.vision_models import ImageGenerationModel


def generate_image_from_text(
        prompt: str = "Google company logo",
) -> object:
    """Example of how to generate an image from a text prompt.

    Args:
        temperature: The temperature of the text prompt.
"""

    model = ImageGenerationModel.from_pretrained("imagegeneration")
    images = model.generate_images(
        prompt=prompt,
        # Optional:
        negative_prompt="bad quality",
        seed=1,
        width=1024,
        height=512,
        guidance_scale=20,
        number_of_images=1,)

    images[0].show()
    print(f"Response from Model: {images[0]}")
    # [END aiplatform_sdk_text_embedding]

    return images


if __name__ == "__main__":
    generate_image_from_text()

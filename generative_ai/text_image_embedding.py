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

# [START aiplatform_sdk_text_image_embedding]
from google.cloud.aiplatform.private_preview.vision_models import ImageGenerationModel


def generate_image_from_text_and_image(
    prompt: str = "Ancient yellowed paper scroll",
) -> object:
    """Example of how to generate an image from a text and an image.

    Args:
        prompt: The prompt to generate an image from."""

    model = ImageGenerationModel.from_pretrained("imagegeneration")
    base_image = model.generate_images("Google company logo", seed=1)
    images = model.generate_images(
        prompt=prompt, seed=1, base_image=base_image[0], guidance_scale=20
    )

    images[0].show()
    print(f"Response from Model: {images[0]}")
    # [END aiplatform_sdk_text_image_embedding]

    return images


if __name__ == "__main__":
    generate_image_from_text_and_image()

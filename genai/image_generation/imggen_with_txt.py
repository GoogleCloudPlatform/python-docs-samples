# Copyright 2025 Google LLC
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

from google.genai.types import Image


def generate_images(output_file: str) -> Image:
    # [START googlegenaisdk_imggen_with_txt]
    from google import genai

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_file = "output-image.png"

    image = client.models.generate_images(
        model="imagen-4.0-generate-preview-05-20",
        prompt="A dog reading a newspaper",
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END googlegenaisdk_imggen_with_txt]
    return image.generated_images[0].image


if __name__ == "__main__":
    generate_images(output_file="test_resources/dog_newspaper.png")

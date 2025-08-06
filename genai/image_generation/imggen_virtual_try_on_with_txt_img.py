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


def virtual_try_on(output_file: str) -> Image:
    # [START googlegenaisdk_imggen_virtual_try_on_with_txt_img]
    from google import genai
    from google.genai.types import RecontextImageSource, ProductImage

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_file = "output-image.png"


    image=client.models.recontext_image(
        model="virtual-try-on-preview-08-04",
        source=RecontextImageSource(
            person_image=Image.from_file(location="test_resources/man.png"),
            product_images=[ProductImage(product_image=Image.from_file(location="test_resources/sweater.jpg"))]
        )
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END googlegenaisdk_imggen_virtual_try_on_with_txt_img]
    return image.generated_images[0].image


if __name__ == "__main__":
    virtual_try_on(output_file="test_resources/man_in_sweater.png")

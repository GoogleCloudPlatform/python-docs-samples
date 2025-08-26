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


def edit_mask_free(output_file: str) -> Image:
    # [START googlegenaisdk_imggen_mask_free_edit_with_txt_img]
    from google import genai
    from google.genai.types import RawReferenceImage, EditImageConfig

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_file = "output-image.png"

    raw_ref = RawReferenceImage(
        reference_image=Image.from_file(location="test_resources/latte.jpg"),
        reference_id=0,
    )

    image = client.models.edit_image(
        model="imagen-3.0-capability-001",
        prompt="Swan latte art in the coffee cup and an assortment of red velvet cupcakes in gold wrappers on the white plate",
        reference_images=[raw_ref],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_DEFAULT",
        ),
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END googlegenaisdk_imggen_mask_free_edit_with_txt_img]
    return image.generated_images[0].image


if __name__ == "__main__":
    edit_mask_free(output_file="output_folder/latte_edit.png")

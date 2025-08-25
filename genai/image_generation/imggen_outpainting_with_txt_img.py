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


def edit_outpainting(output_file: str) -> Image:
    # [START googlegenaisdk_imggen_outpainting_with_txt_img]
    from google import genai
    from google.genai.types import (
        RawReferenceImage,
        MaskReferenceImage,
        MaskReferenceConfig,
        EditImageConfig,
    )

    client = genai.Client()

    # TODO(developer): Update and un-comment below line
    # output_file = "output-image.png"

    raw_ref = RawReferenceImage(
        reference_image=Image.from_file(location="test_resources/living_room.png"),
        reference_id=0,
    )
    mask_ref = MaskReferenceImage(
        reference_id=1,
        reference_image=Image.from_file(location="test_resources/living_room_mask.png"),
        config=MaskReferenceConfig(
            mask_mode="MASK_MODE_USER_PROVIDED",
            mask_dilation=0.03,
        ),
    )

    image = client.models.edit_image(
        model="imagen-3.0-capability-001",
        prompt="A chandelier hanging from the ceiling",
        reference_images=[raw_ref, mask_ref],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_OUTPAINT",
        ),
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END googlegenaisdk_imggen_outpainting_with_txt_img]
    return image.generated_images[0].image


if __name__ == "__main__":
    edit_outpainting(output_file="output_folder/living_room_edit.png")

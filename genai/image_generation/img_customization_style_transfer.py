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

from google import genai

from google.genai.types import Image, EditImageConfig, EditImageResponse, RawReferenceImage


def style_transfer_customization(output_file: str) -> EditImageResponse:
    # [START googlegenaisdk_imagen_style_transfer_customization]
    
    client = genai.Client()

    style_image = Image(gcs_uri="gs://cloud-samples-data/generative-ai/image/teacup-1.png")
    raw_ref_image = RawReferenceImage(reference_image=style_image, reference_id=1)

    image = client.models.edit_image(
        model="imagen-3.0-capability-001",
        prompt="transform the subject in the image so that the teacup[1] is made entirely out of chocolate",
        reference_images=[raw_ref_image],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_DEFAULT",
            number_of_images=1,
            seed=1,
            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            person_generation="ALLOW_ADULT",
        ),
    )

    image.generated_images[0].image._pil_image.save(location=output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END googlegenaisdk_imagen_style_transfer_customization]

    return image


if __name__ == "__main__":
    style_transfer_customization(output_file="test_resources/img_customization.png",)

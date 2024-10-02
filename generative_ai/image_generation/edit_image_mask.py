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

"""Google Cloud Vertex AI sample for editing an image using a mask. The
    edit is applied to the masked area of the image and is saved to a new file.
"""
import os

from vertexai.preview import vision_models

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def edit_image_mask(
    input_file: str,
    mask_file: str,
    output_file: str,
    prompt: str,
) -> vision_models.ImageGenerationResponse:
    # [START generativeaionvertexai_imagen_edit_image_mask]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageGenerationModel

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # input_file = "input-image.png"
    # mask_file = "mask-image.png"
    # output_file = "output-image.png"
    # prompt = "" # The text prompt describing what you want to see.

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagegeneration@002")
    base_img = Image.load_from_file(location=input_file)
    mask_img = Image.load_from_file(location=mask_file)

    images = model.edit_image(
        base_image=base_img,
        mask=mask_img,
        prompt=prompt,
        # Optional parameters
        seed=1,
        # Controls the strength of the prompt.
        # -- 0-9 (low strength), 10-20 (medium strength), 21+ (high strength)
        guidance_scale=21,
        number_of_images=1,
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")
    # Example response:
    # Created output image using 971614 bytes

    # [END generativeaionvertexai_imagen_edit_image_mask]

    return images


if __name__ == "__main__":
    edit_image_mask(
        input_file="test_resources/dog_newspaper.png",
        mask_file="test_resources/dog_newspaper_mask.png",
        output_file="test_resources/dog_book.png",
        prompt="a big book",
    )

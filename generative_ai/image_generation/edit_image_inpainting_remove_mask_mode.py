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

"""Google Cloud Vertex AI sample for editing an image using a mask mode. The
    mask mode is used to automatically select the background, foreground (i.e.,
    the primary subject of the image), or an object based on segmentation class.
    Inpainting can remove the object or background designated by the prompt.
"""
import os

from vertexai.preview import vision_models

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def edit_image_inpainting_remove_mask_mode(
    input_file: str,
    mask_mode: str,
    output_file: str,
    prompt: str,
) -> vision_models.ImageGenerationResponse:
    # [START generativeaionvertexai_imagen_edit_image_inpainting_remove_mask_mode]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageGenerationModel

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # input_file = "input-image.png"
    # mask_mode = "foreground" # 'background', 'foreground', or 'semantic'
    # output_file = "output-image.png"
    # prompt = "sports car" # The text prompt describing what you want to see in the edited image.

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    base_img = Image.load_from_file(location=input_file)

    images = model.edit_image(
        base_image=base_img,
        mask_mode=mask_mode,
        prompt=prompt,
        edit_mode="inpainting-remove",
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")
    # Example response:
    # Created output image using 1279948 bytes

    # [END generativeaionvertexai_imagen_edit_image_inpainting_remove_mask_mode]

    return images


if __name__ == "__main__":
    edit_image_inpainting_remove_mask_mode(
        input_file="test_resources/woman.png",
        mask_mode="foreground",
        output_file="test_resources/sports_car.png",
        prompt="sports car",
    )

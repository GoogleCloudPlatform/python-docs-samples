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
    Inpainting can insert the object or background designated by the prompt.
"""

from vertexai.preview import vision_models


def edit_image_inpainting_insert_mask_mode(
    project_id: str,
    input_file: str,
    mask_mode: str,
    output_file: str,
    prompt: str,
) -> vision_models.ImageGenerationResponse:
    # [START generativeaionvertexai_imagen_edit_image_inpainting_insert_mask_mode]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageGenerationModel

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # input_file = "my-input.png"
    # mask_mode = "background" # 'background', 'foreground', or 'semantic'
    # output_file = "my-output.png"
    # prompt = "" # The text prompt describing what you want to see inserted.

    vertexai.init(project=project_id, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    base_img = Image.load_from_file(location=input_file)

    images = model.edit_image(
        base_image=base_img,
        mask_mode=mask_mode,
        prompt=prompt,
        edit_mode="inpainting-insert",
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    # [END generativeaionvertexai_imagen_edit_image_inpainting_insert_mask_mode]

    return images

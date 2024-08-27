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

"""Google Cloud Vertex AI sample for editing a product image. You can
    modify the background content but preserve the product's appearance.
"""

from vertexai.preview import vision_models


def edit_image_product_image(
    project_id: str,
    input_file: str,
    output_file: str,
    prompt: str,
) -> vision_models.ImageGenerationResponse:
    # [START generativeaionvertexai_imagen_edit_image_product_image]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageGenerationModel

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # input_file = "my-input.png"
    # output_file = "my-output.png"
    # prompt = "" # The text prompt describing what you want to see in the background.

    vertexai.init(project=project_id, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    base_img = Image.load_from_file(location=input_file)

    images = model.edit_image(
        base_image=base_img,
        prompt=prompt,
        edit_mode="product-image",
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    # [END generativeaionvertexai_imagen_edit_image_product_image]

    return images

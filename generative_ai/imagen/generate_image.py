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

"""Google Cloud Vertex AI sample for generating an image using only
    descriptive text as an input.
"""

from vertexai.preview import vision_models


def generate_image(
    project_id: str, output_file: str, prompt: str
) -> vision_models.ImageGenerationResponse:
    # [START generativeaionvertexai_imagen_generate_image]

    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # output_file = "my-output.png"
    # prompt = "" # The text prompt describing what you want to see.

    vertexai.init(project=project_id, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")

    images = model.generate_images(
        prompt=prompt,
        # Optional parameters
        number_of_images=1,
        language="en",
        # You can't use a seed value and watermark at the same time.
        # add_watermark=False,
        # seed=100,
        aspect_ratio="1:1",
        safety_filter_level="block_some",
        person_generation="allow_adult",
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the generated image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    # [END generativeaionvertexai_imagen_generate_image]

    return images

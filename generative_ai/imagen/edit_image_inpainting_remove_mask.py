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

"""Google Cloud Vertex AI sample for editing an image using a mask file.
    Inpainting can remove an object from the masked area.
Example usage:
    python edit_image_inpainting_remove_mask.py --project_id <project-id> \
        --location <location> --input_file <filepath> --mask_file <filepath> \
        --output_file <filepath> [--prompt <text>]
"""

# [START generativeaionvertexai_imagen_edit_image_inpainting_remove_mask]

import argparse

import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel


def edit_image_inpainting_remove_mask(
    project_id: str,
    location: str,
    input_file: str,
    mask_file: str,
    output_file: str,
    prompt: str,
) -> vertexai.preview.vision_models.ImageGenerationResponse:
    """Edit a local image by removing an object using a mask.
    Args:
      project_id: Google Cloud project ID, used to initialize Vertex AI.
      location: Google Cloud region, used to initialize Vertex AI.
      input_file: Local path to the input image file. Image can be in PNG or JPEG format.
      mask_file: Local path to the mask file. Image can be in PNG or JPEG format.
      output_file: Local path to the output image file.
      prompt: The optional text prompt describing the entire image."""

    vertexai.init(project=project_id, location=location)

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    base_img = Image.load_from_file(location=input_file)
    mask_img = Image.load_from_file(location=mask_file)

    images = model.edit_image(
        base_image=base_img,
        mask=mask_img,
        prompt=prompt,
        edit_mode="inpainting-remove",
        # Optional parameters
        # negative_prompt="", # Describes the object being removed (i.e., "person")
    )

    images[0].save(location=output_file)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    return images


# [END generativeaionvertexai_imagen_edit_image_inpainting_remove_mask]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to initialize Vertex AI.",
        default="us-central1",
    )
    parser.add_argument(
        "--input_file",
        help="The local path to the input file (e.g., 'my-input.png').",
        required=True,
    )
    parser.add_argument(
        "--mask_file",
        help="The local path to the mask file (e.g., 'my-mask.png').",
        required=True,
    )
    parser.add_argument(
        "--output_file",
        help="The local path to the output file (e.g., 'my-output.png').",
        required=True,
    )
    parser.add_argument(
        "--prompt",
        help="The optional text prompt describing the entire image.",
        default="",
    )
    args = parser.parse_args()
    edit_image_inpainting_remove_mask(
        args.project_id,
        args.location,
        args.input_file,
        args.mask_file,
        args.output_file,
        args.prompt,
    )

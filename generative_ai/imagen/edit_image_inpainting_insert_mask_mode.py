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
Example usage:
    python edit_image_inpainting_insert_mask_mode.py --project_id <project-id> \
        --location <location> --input_file <filepath> --mask_mode <mode> \
        --output_file <filepath> --prompt <text>
"""

# [START generativeaionvertexai_imagen_edit_image_inpainting_insert_mask_mode]

import argparse

import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel


def edit_image_inpainting_insert_mask_mode(
    project_id: str,
    location: str,
    input_file: str,
    mask_mode: str,
    output_file: str,
    prompt: str,
) -> vertexai.preview.vision_models.ImageGenerationResponse:
    """Edit a local image by inserting an object using a mask.
    Args:
      project_id: Google Cloud project ID, used to initialize Vertex AI.
      location: Google Cloud region, used to initialize Vertex AI.
      input_file: Local path to the input image file. Image can be in PNG or JPEG format.
      mask_mode: Mask generation mode ('background', 'foreground', or 'semantic').
      output_file: Local path to the output image file.
      prompt: The text prompt describing what you want to see inserted."""

    vertexai.init(project=project_id, location=location)

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    base_img = Image.load_from_file(location=input_file)

    images = model.edit_image(
        base_image=base_img,
        mask_mode=mask_mode,
        prompt=prompt,
        edit_mode="inpainting-insert",
        # Optional parameters
        # For semantic mask mode, define the segmentation class IDs:
        # segmentation_classes=[7], # a cat
        # See https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/image-generation#segment-ids.
    )

    images[0].save(location=output_file)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    return images


# [END generativeaionvertexai_imagen_edit_image_inpainting_insert_mask_mode]

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
        "--mask_mode",
        help="The mask generation mode ('background', 'foreground', or 'semantic').",
        required=True,
    )
    parser.add_argument(
        "--output_file",
        help="The local path to the output file (e.g., 'my-output.png').",
        required=True,
    )
    parser.add_argument(
        "--prompt",
        help="The text prompt describing what you want to insert into the automatically masked area.",
        required=True,
    )
    args = parser.parse_args()
    edit_image_inpainting_insert_mask_mode(
        args.project_id,
        args.location,
        args.input_file,
        args.mask_mode,
        args.output_file,
        args.prompt,
    )

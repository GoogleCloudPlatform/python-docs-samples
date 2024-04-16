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
Example usage:
    python generate_image.py --project_id <project-id> --location <location> \
        --output_file <filepath> --prompt <text>
"""

# [START generativeaionvertexai_imagen_generate_image]

import argparse

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel


def generate_image(
    project_id: str, location: str, output_file: str, prompt: str
) -> vertexai.preview.vision_models.ImageGenerationResponse:
    """Generate an image using a text prompt.
    Args:
      project_id: Google Cloud project ID, used to initialize Vertex AI.
      location: Google Cloud region, used to initialize Vertex AI.
      output_file: Local path to the output image file.
      prompt: The text prompt describing what you want to see."""

    vertexai.init(project=project_id, location=location)

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")

    images = model.generate_images(
        prompt=prompt,
        # Optional parameters
        number_of_images=1,
        language="en",  # prompt language
        # By default, a SynthID watermark is added to images, but you can
        # disable it. You can't use a seed value and watermark at the same time.
        # add_watermark=False,
        # seed=100,
        aspect_ratio="1:1",  # "9:16" "16:9" "4:3" "3:4"
        # Adds a filter level to Safety filtering: "block_most" (most strict blocking),
        # "block_some" (default), "block_few", or "block_fewest" (available to
        # allowlisted users only).
        safety_filter_level="block_some",
        # Allows generation of people by the model: "dont_allow" (block
        # all people), "allow_adult" (default; allow adults but not children),
        # "allow_all" (available to allowlisted users only; allow adults and children)
        person_generation="allow_adult",
    )

    images[0].save(location=output_file, include_generation_parameters=True)

    # Optional. View the generated image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    return images


# [END generativeaionvertexai_imagen_generate_image]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to initialize Vertex AI.",
        default="us-central1",
    )
    parser.add_argument(
        "--output_file",
        help="The local path to the output file (e.g., 'my-output.png').",
        required=True,
    )
    parser.add_argument(
        "--prompt",
        help="The text prompt describing what you want to see (e.g., 'a dog reading a newspaper').",
        required=True,
    )
    args = parser.parse_args()
    generate_image(
        args.project_id,
        args.location,
        args.output_file,
        args.prompt,
    )

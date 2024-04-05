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

"""Google Cloud Vertex AI sample for getting short-form image captions.
Example usage:
    python get_short_form_image_captions.py --project_id <project-id> --location <location> \
        --input_file <filepath>
"""

# [START aiplatform_imagen_get_short_form_image_captions]
# [START generativeaionvertexai_imagen_get_short_form_image_captions]

import argparse

import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel


def get_short_form_image_captions(
    project_id: str, location: str, input_file: str
) -> list:
    """Get short-form captions for a local image.
    Args:
      project_id: Google Cloud project ID, used to initialize Vertex AI.
      location: Google Cloud region, used to initialize Vertex AI.
      input_file: Local path to the input image file."""

    vertexai.init(project=project_id, location=location)

    model = ImageTextModel.from_pretrained("imagetext@001")
    source_img = Image.load_from_file(location=input_file)

    captions = model.get_captions(
        image=source_img,
        # Optional parameters
        language="en",
        number_of_results=1,
    )

    print(captions)

    return captions


# [END generativeaionvertexai_imagen_get_short_form_image_captions]
# [END aiplatform_imagen_get_short_form_image_captions]

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
    args = parser.parse_args()
    get_short_form_image_captions(
        args.project_id,
        args.location,
        args.input_file,
    )

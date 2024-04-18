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
"""


def get_short_form_image_captions(project_id: str, input_file: str) -> list:

    # [START generativeaionvertexai_imagen_get_short_form_image_captions]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageTextModel

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # input_file = "my-input.png"

    vertexai.init(project=project_id, location="us-central1")

    model = ImageTextModel.from_pretrained("imagetext@001")
    source_img = Image.load_from_file(location=input_file)

    captions = model.get_captions(
        image=source_img,
        # Optional parameters
        language="en",
        number_of_results=1,
    )

    print(captions)

    # [END generativeaionvertexai_imagen_get_short_form_image_captions]

    return captions

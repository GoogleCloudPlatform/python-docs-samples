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

"""Google Cloud Vertex AI sample for getting short-form responses to a
    question about an image.
"""
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_short_form_image_responses(input_file: str, question: str) -> list:
    # [START generativeaionvertexai_imagen_get_short_form_image_responses]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageTextModel

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # input_file = "input-image.png"
    # question = "" # The question about the contents of the image.

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = ImageTextModel.from_pretrained("imagetext@001")
    source_img = Image.load_from_file(location=input_file)

    answers = model.ask_question(
        image=source_img,
        question=question,
        # Optional parameters
        number_of_results=1,
    )

    print(answers)
    # Example response:
    # ['tabby']

    # [END generativeaionvertexai_imagen_get_short_form_image_responses]

    return answers


if __name__ == "__main__":
    get_short_form_image_responses(
        input_file="test_resources/cat.png",
        question="What breed of cat is this a picture of?",
    )

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

import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_text() -> str:
    # [START generativeaionvertexai_gemini_safety_settings]
    import vertexai

    from vertexai.generative_models import (
        GenerativeModel,
        HarmCategory,
        HarmBlockThreshold,
        Part,
        SafetySetting,
    )

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    # Safety config
    safety_config = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]

    image_file = Part.from_uri(
        "gs://cloud-samples-data/generative-ai/image/scones.jpg", "image/jpeg"
    )

    # Generate content
    response = model.generate_content(
        [image_file, "What is in this image?"],
        safety_settings=safety_config,
    )

    print(response.text)
    print(response.candidates[0].safety_ratings)
    # Example response:
    # The image contains a beautiful arrangement of blueberry scones, flowers, coffee, and blueberries.
    # The scene is set on a rustic blue background. The image evokes a sense of comfort and indulgence.
    # ...

    # [END generativeaionvertexai_gemini_safety_settings]
    return response.text


if __name__ == "__main__":
    generate_text()

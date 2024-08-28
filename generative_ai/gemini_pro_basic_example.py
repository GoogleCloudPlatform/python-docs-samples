# Copyright 2023 Google LLC
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


def generate_text() -> None:
    # [START generativeaionvertexai_gemini_pro_example]
    import vertexai

    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update project_id and location
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    image_file = Part.from_uri(
        "gs://cloud-samples-data/generative-ai/image/scones.jpg", "image/jpeg"
    )

    # Query the model
    response = model.generate_content([image_file, "what is this image?"])
    print(response.text)

    # [END generativeaionvertexai_gemini_pro_example]
    return response.text


if __name__ == "__main__":
    generate_text()

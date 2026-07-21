# Copyright 2026 Google LLC
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

# [START aiplatform_genai_gemini_set_labels]

import os

from google import genai

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("LOCATION_ID")
GEMINI_MODEL = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")


def generate_content() -> genai.types.GenerateContentResponse:

    genai_client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)

    labels = {
        "environment": "testing",
        "feature": "genai",
        "model": "gemini",
    }

    config = genai.types.GenerateContentConfig(temperature=0.4, labels=labels)

    response = genai_client.models.generate_content(
        model=GEMINI_MODEL, contents="What is Generative AI?", config=config
    )

    print(response.text)
    return response


# [END aiplatform_genai_gemini_set_labels]


if __name__ == "__main__":
    generate_content()

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from google.cloud import aiplatform

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


# [START aiplatform_translate]


# TODO (Developer) Uncomment the following line and replace the value
# PROJECT_ID = "your-project-id"
def translate(
    text: str, source_language_code: str = "en", target_language_code: str = "fr"
):
    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/text-translation"
    )

    # Initialize the request
    instances = [
        {
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "contents": [text],
            "mimeType": "text/plain",
            "model": f"projects/{PROJECT_ID}/locations/us-central1/models/general/translation-llm",
        }
    ]

    # Make the prediction
    response = endpoint.predict(instances=instances)

    # Handle the response
    print(response)


# [END aiplatform_translate]

if __name__ == "__main__":
    translate(
        "Hello, how are you?",
    )

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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


# [START aiplatform_translate_api]
def translate(
    text: str, source_language_code: str = "en", target_language_code: str = "fr"
):
    # Create a client
    endpoint = aiplatform.Endpoint(
        f"projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/translate-llm"
    )
    # Initialize the request
    instances = [
        {
            "reference_sentence_config": {
                "reference_sentence_pair_lists": [
                    {
                        "reference_sentence_pairs": [
                            {
                                "source_sentence": "How are you?",  # Example: 'Hello! How are you?'
                                "target_sentence": "Comment ça va?",  # Example translation: 'Comment ça va?'
                            },
                            {
                                "source_sentence": "I would like a cup of coffee.",
                                "target_sentence": "Je voudrais une tasse de café.",  # Example translation: 'Je voudrais une tasse de café.'
                            },
                        ]
                    }
                ],
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            },
            "contents": [text],  # The text you want to translate
        }
    ]
    # Make the request
    response = endpoint.predict(instances=instances)
    # Handle the response
    print(response)


# [END aiplatform_translate_api]

if __name__ == "__main__":
    translate("Hello! How are you?")

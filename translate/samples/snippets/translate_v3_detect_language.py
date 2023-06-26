# Copyright 2020 Google LLC
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

# [START translate_v3_detect_language]
from google.cloud import translate


def detect_language(
    project_id: str = "YOUR_PROJECT_ID",
) -> translate.DetectLanguageResponse:
    """Detecting the language of a text string.

    Args:
        project_id: The GCP project ID.

    Returns:
        The detected language of the text.
    """
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.detect_language(
        content="Hello, world!",
        parent=parent,
        mime_type="text/plain",  # mime types: text/plain, text/html
    )

    # Display list of detected languages sorted by detection confidence.
    # The most probable language is first.
    for language in response.languages:
        # The language detected
        print(f"Language code: {language.language_code}")
        # Confidence of detection result for this language
        print(f"Confidence: {language.confidence}")

    return response


# [END translate_v3_detect_language]

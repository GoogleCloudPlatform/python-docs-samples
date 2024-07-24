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

# [START speech_create_recognizer]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def create_recognizer(recognizer_id: str) -> cloud_speech.Recognizer:
    """
    Method creates a recognizer with an unique ID and default recognition
    configuration. The recognizer is created in the global location of the project specified by the
    PROJECT_ID environment variable.

    Args:
        recognizer_id (str): The unique identifier for the recognizer to be created.

    Returns:
        cloud_speech.Recognizer: The created recognizer object with configuration.

    """

    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{PROJECT_ID}/locations/global",
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            default_recognition_config=cloud_speech.RecognitionConfig(
                language_codes=["en-US"], model="long"
            ),
        ),
    )
    # Sends the request to create a recognizer and waits for the operation to complete
    operation = client.create_recognizer(request=request)
    recognizer = operation.result()

    print("Created Recognizer:", recognizer.name)
    return recognizer


# [END speech_create_recognizer]


if __name__ == "__main__":
    custom_recognizer_id = "recognizer-custom-id"
    create_recognizer(custom_recognizer_id)

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START speech_enable_cmek]
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def enable_cmek(
    kms_key_name: str,
) -> cloud_speech.Config:
    """Enable Customer-Managed Encryption Keys (CMEK) in a project and region.
    Args:
        kms_key_name (str): The full resource name of the KMS key to be used for encryption.
            E.g,: projects/{PROJECT_ID}/locations/{LOCATION}/keyRings/{KEY_RING}/cryptoKeys/{KEY_NAME}
    Returns:
        cloud_speech.Config: The response from the update configuration request,
        containing the updated configuration details.
    """
    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.UpdateConfigRequest(
        config=cloud_speech.Config(
            name=f"projects/{PROJECT_ID}/locations/global/config",
            kms_key_name=kms_key_name,
        ),
        update_mask={"paths": ["kms_key_name"]},
    )

    # Updates the KMS key for the project and region.
    response = client.update_config(request=request)

    print(f"Updated KMS key: {response.kms_key_name}")
    return response


# [END speech_enable_cmek]


if __name__ == "__main__":
    PROJECT_ID = "your-project-id"
    LOCATION = "global"
    KEY_RING = "your-key-ring"
    KEY_NAME = "your-key-name"
    key_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/keyRings/{KEY_RING}/cryptoKeys/{KEY_NAME}"
    enable_cmek(key_name)

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


import argparse

# [START speech_enable_cmek]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def enable_cmek(
    project_id: str,
    kms_key_name: str,
) -> cloud_speech.RecognizeResponse:
    """Enable CMEK in a project and region."""
    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.UpdateConfigRequest(
        config=cloud_speech.Config(
            name=f"projects/{project_id}/locations/global/config",
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
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="GCP Project ID")
    parser.add_argument("kms_key_name", help="Resource path of a KMS key")
    args = parser.parse_args()
    enable_cmek(args.project_id, args.kms_key_name)

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

# [START speech_transcribe_batch_gcs_input_inline_output_v2]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def transcribe_batch_gcs_input_inline_output_v2(
    project_id: str,
    gcs_uri: str,
) -> cloud_speech.BatchRecognizeResults:
    """Transcribes audio from a Google Cloud Storage URI.

    Args:
        project_id: The Google Cloud project ID.
        gcs_uri: The Google Cloud Storage URI.

    Returns:
        The RecognizeResponse.
    """
    # Instantiates a client
    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    # Transcribes the audio into text
    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)

    for result in response.results[gcs_uri].transcript.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response.results[gcs_uri].transcript


# [END speech_transcribe_batch_gcs_input_inline_output_v2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="GCP Project ID")
    parser.add_argument("gcs_uri", help="URI to GCS file")
    args = parser.parse_args()
    transcribe_batch_gcs_input_inline_output_v2(args.project_id, args.gcs_uri)

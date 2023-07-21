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

# [START speech_transcribe_batch_multiple_files_v2]
import re
from typing import List

from google.cloud import storage
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def transcribe_batch_multiple_files_v2(
    project_id: str,
    gcs_uris: List[str],
    gcs_output_path: str,
) -> cloud_speech.BatchRecognizeResponse:
    """Transcribes audio from a Google Cloud Storage URI.

    Args:
        project_id: The Google Cloud project ID.
        gcs_uris: The Google Cloud Storage URIs to transcribe.
        gcs_output_path: The Cloud Storage URI to which to write the transcript.

    Returns:
        The BatchRecognizeResponse message.
    """
    # Instantiates a client
    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )

    files = [
        cloud_speech.BatchRecognizeFileMetadata(uri=uri)
        for uri in gcs_uris
    ]

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        files=files,
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            gcs_output_config=cloud_speech.GcsOutputConfig(
                uri=gcs_output_path,
            ),
        ),
    )

    # Transcribes the audio into text
    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)

    print("Operation finished. Fetching results from:")
    for uri in gcs_uris:
        file_results = response.results[uri]
        print(f"  {file_results.uri}...")
        output_bucket, output_object = re.match(
            r"gs://([^/]+)/(.*)", file_results.uri
        ).group(1, 2)

        # Instantiates a Cloud Storage client
        storage_client = storage.Client()

        # Fetch results from Cloud Storage
        bucket = storage_client.bucket(output_bucket)
        blob = bucket.blob(output_object)
        results_bytes = blob.download_as_bytes()
        batch_recognize_results = cloud_speech.BatchRecognizeResults.from_json(
            results_bytes, ignore_unknown_fields=True
        )

        for result in batch_recognize_results.results:
            print(f"     Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_transcribe_batch_multiple_files_v2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="GCP Project ID")
    parser.add_argument("gcs_uri", nargs="+", help="URI to GCS file")
    parser.add_argument(
        "gcs_output_path", help="GCS URI to which to write the transcript"
    )
    args = parser.parse_args()
    transcribe_batch_multiple_files_v2(
        args.project_id, args.gcs_uri, args.gcs_output_path
    )

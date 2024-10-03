# Copyright 2021 Google LLC
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

# [START speech_transcribe_with_speech_to_storage_beta]

from google.cloud import speech
from google.cloud import storage
from google.cloud.speech_v1 import types


def export_transcript_to_storage_beta(
    audio_uri: str,
    output_bucket_name: str,
    output_filename: str,
) -> types.LongRunningRecognizeResponse:
    """Transcribes an audio file from Cloud Storage and exports the transcript to Cloud Storage bucket.
    Args:
        audio_uri (str): The Cloud Storage URI of the input audio, e.g., gs://[BUCKET]/[FILE]
        output_bucket_name (str): Name of the Cloud Storage bucket to store the output transcript.
        output_filename (str): Name of the output file to store the transcript.
    Returns:
        types.LongRunningRecognizeResponse: The response containing the transcription results.
    """

    audio = speech.RecognitionAudio(uri=audio_uri)
    output_storage_uri = f"gs://{output_bucket_name}/{output_filename}"

    # Pass in the URI of the Cloud Storage bucket to hold the transcription
    output_config = speech.TranscriptOutputConfig(gcs_uri=output_storage_uri)

    # Speech configuration object
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    # Compose the long-running request
    request = speech.LongRunningRecognizeRequest(
        audio=audio, config=config, output_config=output_config
    )

    # Create the speech client
    speech_client = speech.SpeechClient()
    # Create the storage client
    storage_client = storage.Client()

    # Run the recognizer to export transcript
    operation = speech_client.long_running_recognize(request=request)
    print("Waiting for operation to complete...")
    operation.result(timeout=90)

    # Get bucket with name
    bucket = storage_client.get_bucket(output_bucket_name)
    # Get blob (file) from bucket
    blob = bucket.get_blob(output_filename)

    # Get content as bytes
    results_bytes = blob.download_as_bytes()
    # Get transcript exported in storage bucket
    storage_transcript = types.LongRunningRecognizeResponse.from_json(
        results_bytes, ignore_unknown_fields=True
    )

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in storage_transcript.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Confidence: {result.alternatives[0].confidence}")

    # [END speech_transcribe_with_speech_to_storage_beta]
    return storage_transcript.results


if __name__ == "__main__":
    export_transcript_to_storage_beta(
        audio_uri="gs://cloud-samples-data/speech/commercial_mono.wav",
        output_bucket_name="bucket-unique-name",
        output_filename="output-transcript-filename",
    )

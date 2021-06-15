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

from google.cloud import speech_v1p1beta1 as speech


def export_transcript_to_storage_beta(
    input_storage_uri, output_storage_uri, encoding, sample_rate_hertz, language_code
):

    # input_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    audio = speech.RecognitionAudio(uri=input_storage_uri)

    # Pass in the URI of the Cloud Storage bucket to hold the transcription
    output_config = speech.TranscriptOutputConfig(gcs_uri=output_storage_uri)

    # Speech configuration object
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    # Compose the long-running request
    request = speech.LongRunningRecognizeRequest(
        audio=audio, config=config, output_config=output_config
    )

    # Create the speech client
    speech_client = speech.SpeechClient()

    operation = speech_client.long_running_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    # [END speech_transcribe_with_speech_to_storage_beta]
    return response.results[0].alternatives[0].transcript

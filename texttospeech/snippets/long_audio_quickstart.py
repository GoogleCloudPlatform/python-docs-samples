# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import texttospeech


def synthesize_long_audio(project_id: str, output_gcs_uri: str) -> None:
    """
    Synthesizes long input, writing the resulting audio to `output_gcs_uri`.

    Args:
        project_id: ID or number of the Google Cloud project you want to use.
        output_gcs_uri: Specifies a Cloud Storage URI for the synthesis results.
            Must be specified in the format:
            ``gs://bucket_name/object_name``, and the bucket must
            already exist.
    """

    client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    input = texttospeech.SynthesisInput(
        text="Test input. Replace this with any text you want to synthesize, up to 1 million bytes long!"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Standard-A"
    )

    parent = f"projects/{project_id}/locations/us-central1"

    request = texttospeech.SynthesizeLongAudioRequest(
        parent=parent,
        input=input,
        audio_config=audio_config,
        voice=voice,
        output_gcs_uri=output_gcs_uri,
    )

    operation = client.synthesize_long_audio(request=request)
    # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
    # If the operation times out, that likely means there was an error. In that case, inspect the error, and try again.
    result = operation.result(timeout=300)
    print(
        "\nFinished processing, check your GCS bucket to find your audio file! Printing what should be an empty result: ",
        result,
    )

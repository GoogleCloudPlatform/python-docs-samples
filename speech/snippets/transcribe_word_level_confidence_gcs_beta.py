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

# [START speech_transcribe_word_level_confidence_gcs_beta]

from google.cloud import speech_v1p1beta1 as speech


def transcribe_file_with_word_level_confidence(audio_uri: str) -> str:
    """Transcribe a remote audio file with word level confidence.
    Args:
        audio_uri (str): The Cloud Storage URI of the input audio.
            E.g., gs://[BUCKET]/[FILE]
    Returns:
        The generated transcript from the audio file provided with word level confidence.
    """

    client = speech.SpeechClient()

    # Configure request to enable word level confidence
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_confidence=True,  # Enable word level confidence
    )

    # Set the remote path for the audio file
    audio = speech.RecognitionAudio(uri=audio_uri)

    # Use non-blocking call for getting file transcription
    response = client.long_running_recognize(config=config, audio=audio).result(
        timeout=300
    )

    transcript_builder = []
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        transcript_builder.append("-" * 20)
        transcript_builder.append(f"\nFirst alternative of result {i}")
        transcript_builder.append(f"\nTranscript: {alternative.transcript}")
        transcript_builder.append(
            "\nFirst Word and Confidence: ({}, {})".format(
                alternative.words[0].word, alternative.words[0].confidence
            )
        )

    transcript = "".join(transcript_builder)
    print(transcript)

    return transcript


# [END speech_transcribe_word_level_confidence_gcs_beta]

if __name__ == "__main__":
    transcribe_file_with_word_level_confidence(
        "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    )

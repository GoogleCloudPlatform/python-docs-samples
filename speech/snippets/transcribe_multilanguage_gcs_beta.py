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

# [START speech_transcribe_multilanguage_gcs_beta]

from google.cloud import speech_v1p1beta1 as speech


def transcribe_file_with_multilanguage_gcs(audio_uri: str) -> str:
    """Transcribe a remote audio file with multi-language recognition
    Args:
        audio_uri (str): The Google Cloud Storage path to an audio file.
            E.g., gs://[BUCKET]/[FILE]
    Returns:
        str: The generated transcript from the audio file provided.
    """

    client = speech.SpeechClient()

    first_language = "es-ES"
    alternate_languages = ["en-US", "fr-FR"]

    # Configure request to enable multiple languages
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code=first_language,
        alternative_language_codes=alternate_languages,
    )

    # Set the remote path for the audio file
    audio = speech.RecognitionAudio(uri=audio_uri)

    # Use non-blocking call for getting file transcription
    response = client.long_running_recognize(
        config=recognition_config, audio=audio
    ).result(timeout=300)

    transcript_builder = []
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        transcript_builder.append("-" * 20 + "\n")
        transcript_builder.append(f"First alternative of result {i}: {alternative}")
        transcript_builder.append(f"Transcript: {alternative.transcript} \n")

    transcript = "".join(transcript_builder)
    print(transcript)

    return transcript


# [END speech_transcribe_multilanguage_gcs_beta]

if __name__ == "__main__":
    transcribe_file_with_multilanguage_gcs(
        "gs://cloud-samples-data/speech/multi_es.flac"
    )

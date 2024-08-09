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

# [START speech_transcribe_diarization_gcs_beta]

from google.cloud import speech


def transcribe_diarization_gcs_beta(audio_uri: str) -> bool:
    """Transcribe a remote audio file (stored in Google Cloud Storage) using speaker diarization.
    Args:
        audio_uri (str): The Google Cloud Storage path to an audio file.
            E.g., gs://[BUCKET]/[FILE]
    Returns:
        True if the operation successfully completed, False otherwise.
    """

    client = speech.SpeechClient()
    # Enhance diarization config with more speaker counts and details
    speaker_diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,  # Set minimum number of speakers
        max_speaker_count=2,  # Adjust max speakers based on expected number of speakers
    )

    # Configure recognition with enhanced audio settings
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        sample_rate_hertz=8000,
        diarization_config=speaker_diarization_config,
    )

    # Set the remote path for the audio file
    audio = speech.RecognitionAudio(
        uri=audio_uri,
    )

    # Use non-blocking call for getting file transcription
    response = client.long_running_recognize(
        config=recognition_config, audio=audio
    ).result(timeout=300)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result
    result = response.results[-1]
    words_info = result.alternatives[0].words

    # Print the output
    for word_info in words_info:
        print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")
    return True


# [END speech_transcribe_diarization_gcs_beta]

if __name__ == "__main__":
    transcribe_diarization_gcs_beta(
        audio_uri="gs://cloud-samples-data/speech/commercial_mono.wav"
    )

# Copyright 2017 Google LLC
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

"""Google Cloud Speech API sample that demonstrates word time offsets."""

from google.cloud import speech


def transcribe_file_with_word_time_offsets(
    audio_file: str,
) -> speech.RecognizeResponse:
    """Transcribe the given audio file synchronously and output the word time
    offsets.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/audio.wav"
    Returns:
        speech.RecognizeResponse: The response containing the transcription results with word time offsets.
    """

    client = speech.SpeechClient()

    with open(audio_file, "rb") as file:
        audio_content = file.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )

    return response


# [START speech_transcribe_async_word_time_offsets_gcs]
def transcribe_gcs_with_word_time_offsets(
    audio_uri: str,
) -> speech.RecognizeResponse:
    """Transcribe the given audio file asynchronously and output the word time
    offsets.
    Args:
        audio_uri (str): The Google Cloud Storage URI of the input audio file.
            E.g., gs://[BUCKET]/[FILE]
    Returns:
        speech.RecognizeResponse: The response containing the transcription results with word time offsets.
    """
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    for result in result.results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
        print(f"Confidence: {alternative.confidence}")

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )

    return result


# [END speech_transcribe_async_word_time_offsets_gcs]


if __name__ == "__main__":
    # It could be a local path like: path_to_file = "resources/audio.raw"
    path_to_file = "gs://cloud-samples-data/speech/audio.flac"
    if path_to_file.startswith("gs://"):
        transcribe_gcs_with_word_time_offsets(path_to_file)
    else:
        transcribe_file_with_word_time_offsets(path_to_file)

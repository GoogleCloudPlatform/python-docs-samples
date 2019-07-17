#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample that demonstrates enhanced models
and recognition metadata.

Example usage:
    python beta_snippets.py enhanced-model
    python beta_snippets.py metadata
    python beta_snippets.py punctuation
    python beta_snippets.py diarization
    python beta_snippets.py multi-channel
    python beta_snippets.py multi-language
    python beta_snippets.py word-level-conf
"""

import argparse
import io


def transcribe_file_with_enhanced_model():
    """Transcribe the given audio file using an enhanced model."""
    # [START speech_transcribe_enhanced_model_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/commercial_mono.wav'

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model='phone_call')

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print(u'First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_enhanced_model_beta]


def transcribe_file_with_metadata():
    """Send a request that includes recognition metadata."""
    # [START speech_transcribe_recognition_metadata_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/commercial_mono.wav'

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    # Here we construct a recognition metadata object.
    # Most metadata fields are specified as enums that can be found
    # in speech.enums.RecognitionMetadata
    metadata = speech.types.RecognitionMetadata()
    metadata.interaction_type = (
        speech.enums.RecognitionMetadata.InteractionType.DISCUSSION)
    metadata.microphone_distance = (
        speech.enums.RecognitionMetadata.MicrophoneDistance.NEARFIELD)
    metadata.recording_device_type = (
        speech.enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE)
    # Some metadata fields are free form strings
    metadata.recording_device_name = "Pixel 2 XL"
    # And some are integers, for instance the 6 digit NAICS code
    # https://www.naics.com/search/
    metadata.industry_naics_code_of_audio = 519190

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Add this in the request to send metadata.
        metadata=metadata)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print(u'First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_recognition_metadata_beta]


def transcribe_file_with_auto_punctuation():
    """Transcribe the given audio file with auto punctuation enabled."""
    # [START speech_transcribe_auto_punctuation_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/commercial_mono.wav'

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print(u'First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_auto_punctuation_beta]


def transcribe_file_with_diarization():
    """Transcribe the given audio file synchronously with diarization."""
    # [START speech_transcribe_diarization_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/commercial_mono.wav'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2)

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    for word_info in words_info:
        print(u"word: '{}', speaker_tag: {}".format(
            word_info.word, word_info.speaker_tag))
    # [END speech_transcribe_diarization_beta]


def transcribe_file_with_multichannel():
    """Transcribe the given audio file synchronously with
      multi channel."""
    # [START speech_transcribe_multichannel_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/Google_Gnome.wav'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        audio_channel_count=1,
        enable_separate_recognition_per_channel=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
        print(u'Channel Tag: {}'.format(result.channel_tag))
    # [END speech_transcribe_multichannel_beta]


def transcribe_file_with_multilanguage():
    """Transcribe the given audio file synchronously with
      multi language."""
    # [START speech_transcribe_multilanguage_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/multi.wav'
    first_lang = 'en-US'
    second_lang = 'es'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        audio_channel_count=2,
        language_code=first_lang,
        alternative_language_codes=[second_lang])

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print(u'First alternative of result {}: {}'.format(i, alternative))
        print(u'Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_multilanguage_beta]


def transcribe_file_with_word_level_confidence():
    """Transcribe the given audio file synchronously with
      word level confidence."""
    # [START speech_transcribe_word_level_confidence_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    speech_file = 'resources/Google_Gnome.wav'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_confidence=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
        print(u'First Word and Confidence: ({}, {})'.format(
            alternative.words[0].word, alternative.words[0].confidence))
    # [END speech_transcribe_word_level_confidence_beta]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command')

    args = parser.parse_args()

    if args.command == 'enhanced-model':
        transcribe_file_with_enhanced_model()
    elif args.command == 'metadata':
        transcribe_file_with_metadata()
    elif args.command == 'punctuation':
        transcribe_file_with_auto_punctuation()
    elif args.command == 'diarization':
        transcribe_file_with_diarization()
    elif args.command == 'multi-channel':
        transcribe_file_with_multichannel()
    elif args.command == 'multi-language':
        transcribe_file_with_multilanguage()
    elif args.command == 'word-level-conf':
        transcribe_file_with_word_level_confidence()

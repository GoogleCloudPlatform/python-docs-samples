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
    python beta_snippets.py enhanced-model resources/commercial_mono.wav
    python beta_snippets.py metadata resources/commercial_mono.wav
    python beta_snippets.py punctuation resources/commercial_mono.wav
    python beta_snippets.py diarization resources/commercial_mono.wav
    python beta_snippets.py multi-channel resources/commercial_mono.wav
    python beta_snippets.py multi-language resources/multi.wav en-US es
    python beta_snippets.py word-level-conf resources/commercial_mono.wav
"""

import argparse
import io


def transcribe_file_with_enhanced_model(speech_file):
    """Transcribe the given audio file using an enhanced model."""
    # [START speech_transcribe_file_with_enhanced_model]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model='phone_call')

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_file_with_enhanced_model]


def transcribe_file_with_metadata(speech_file):
    """Send a request that includes recognition metadata."""
    # [START speech_transcribe_file_with_metadata]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'

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
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_file_with_metadata]


def transcribe_file_with_auto_punctuation(speech_file):
    """Transcribe the given audio file with auto punctuation enabled."""
    # [START speech_transcribe_file_with_auto_punctuation]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'

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
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_file_with_auto_punctuation]


def transcribe_file_with_diarization(speech_file):
    """Transcribe the given audio file synchronously with diarization."""
    # [START speech_transcribe_diarization]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2)

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}: {}'
              .format(i, alternative.transcript))
        print('Speaker Tag for the first word: {}'
              .format(alternative.words[0].speaker_tag))
    # [END speech_transcribe_diarization]


def transcribe_file_with_multichannel(speech_file):
    """Transcribe the given audio file synchronously with
      multi channel."""
    # [START speech_transcribe_multichannel]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'

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
    # [END speech_transcribe_multichannel]


def transcribe_file_with_multilanguage(speech_file, first_lang, second_lang):
    """Transcribe the given audio file synchronously with
      multi language."""
    # [START speech_transcribe_multilanguage]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'
    # first_lang = first language code, e,g, 'en-US'
    # second_lang = first language code, e,g, 'es'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,
        language_code=first_lang,
        alternative_language_codes=[second_lang])

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}: {}'.format(i, alternative))
        print(u'Transcript: {}'.format(alternative.transcript))
    # [END speech_transcribe_multilanguage]


def transcribe_file_with_word_level_confidence(speech_file):
    """Transcribe the given audio file synchronously with
      word level confidence."""
    # [START speech_transcribe_word_level_confidence]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    # TODO(developer): Uncomment and set to a path to your audio file.
    # speech_file = 'path/to/file.wav'

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
    # [END speech_transcribe_word_level_confidence]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command')
    parser.add_argument(
        'path', help='File for audio file to be recognized')
    parser.add_argument(
        'first', help='First language in audio file to be recognized',
        nargs='?')
    parser.add_argument(
        'second', help='Second language in audio file to be recognized',
        nargs='?')

    args = parser.parse_args()

    if args.command == 'enhanced-model':
        transcribe_file_with_enhanced_model(args.path)
    elif args.command == 'metadata':
        transcribe_file_with_metadata(args.path)
    elif args.command == 'punctuation':
        transcribe_file_with_auto_punctuation(args.path)
    elif args.command == 'diarization':
        transcribe_file_with_diarization(args.path)
    elif args.command == 'multi-channel':
        transcribe_file_with_multichannel(args.path)
    elif args.command == 'multi-language':
        transcribe_file_with_multilanguage(args.path, args.first, args.second)
    elif args.command == 'word-level-conf':
        transcribe_file_with_word_level_confidence(args.path)

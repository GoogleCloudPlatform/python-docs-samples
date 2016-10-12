#!/usr/bin/env python

# Copyright 2016 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations with the
Google Cloud Translate API

For more information, the documentation at
https://cloud.google.com/translate/docs.
"""

import argparse

from google.cloud import translate


def detect_language(api_key, text):
    """Detects the text's language."""
    translate_client = translate.Client(api_key)

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    print('Text: {}'.format(text))
    print('Confidence: {}'.format(result['confidence']))
    print('Language: {}'.format(result['language']))


def list_languages(api_key):
    """Lists all available languages."""
    translate_client = translate.Client(api_key)

    results = translate_client.get_languages()

    for language in results:
        print(u'{name} ({language})'.format(**language))


def list_languages_with_target(api_key, target):
    """Lists all available languages and localizes them to the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client(api_key)

    results = translate_client.get_languages(target_language=target)

    for language in results:
        print(u'{name} ({language})'.format(**language))


def translate_text(api_key, target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client(api_key)

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('api_key', help='Your API key.')
    subparsers = parser.add_subparsers(dest='command')

    detect_langage_parser = subparsers.add_parser(
        'detect-language', help=detect_language.__doc__)
    detect_langage_parser.add_argument('text')

    list_languages_parser = subparsers.add_parser(
        'list-languages', help=list_languages.__doc__)

    list_languages_with_target_parser = subparsers.add_parser(
        'list-languages-with-target', help=list_languages_with_target.__doc__)
    list_languages_with_target_parser.add_argument('target')

    translate_text_parser = subparsers.add_parser(
        'translate-text', help=translate_text.__doc__)
    translate_text_parser.add_argument('target')
    translate_text_parser.add_argument('text')

    args = parser.parse_args()

    if args.command == 'detect-language':
        detect_language(args.api_key, args.text)
    elif args.command == 'list-languages':
        list_languages(args.api_key)
    elif args.command == 'list-languages-with-target':
        list_languages_with_target(args.api_key, args.target)
    elif args.command == 'translate-text':
        translate_text(args.api_key, args.target, args.text)

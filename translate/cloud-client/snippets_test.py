# -*- coding: utf-8 -*-

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


def test_detect_language(capsys):
    # [START translate_detect_language]
    from google.cloud import translate

    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    text = 'Hæ sæta'
    result = translate_client.detect_language(text)

    print('Text: {}'.format(text))
    print('Confidence: {}'.format(result['confidence']))
    print('Language: {}'.format(result['language']))
    # [END translate_detect_language]

    out, _ = capsys.readouterr()
    assert 'is' in out


def test_list_languages(capsys):
    # [START translate_list_codes]
    from google.cloud import translate

    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print(u'{name} ({language})'.format(**language))
    # [END translate_list_codes]

    out, _ = capsys.readouterr()
    assert 'Icelandic (is)' in out


def test_list_languages_with_target(capsys):
    # [START translate_list_language_names]
    from google.cloud import translate

    translate_client = translate.Client()

    target = 'is'  # Target must be an ISO 639-1 language code.
    results = translate_client.get_languages(target_language=target)

    for language in results:
        print(u'{name} ({language})'.format(**language))
    # [END translate_list_language_names]

    out, _ = capsys.readouterr()
    assert u'íslenska (is)' in out


def test_translate_text(capsys):
    # [START translate_text_with_model]
    import six
    from google.cloud import translate

    translate_client = translate.Client()

    text = 'Hello world'
    target = 'is'  # Target must be an ISO 639-1 language code.
    model = translate.NMT
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target, model=model)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    # [END translate_text_with_model]

    out, _ = capsys.readouterr()
    assert u'Halló heimur' in out


def test_translate_utf8(capsys):
    # [START translate_translate_text]
    import six
    from google.cloud import translate

    translate_client = translate.Client()

    target = 'en'  # Target must be an ISO 639-1 language code.
    text = u'나는 파인애플을 좋아한다.'
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    # [END translate_translate_text]

    out, _ = capsys.readouterr()
    assert u'I like pineapples.' in out

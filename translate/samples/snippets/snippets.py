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

from __future__ import annotations

import argparse


# [START translate_detect_language]
def detect_language(text: str) -> dict:
    """Detects the text's language."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    print(f"Text: {text}")
    print("Confidence: {}".format(result["confidence"]))
    print("Language: {}".format(result["language"]))

    return result


# [END translate_detect_language]


# [START translate_list_codes]
def list_languages() -> dict:
    """Lists all available languages."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print("{name} ({language})".format(**language))

    return results


# [END translate_list_codes]


# [START translate_list_language_names]
def list_languages_with_target(target: str) -> dict:
    """Lists all available languages and localizes them to the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    results = translate_client.get_languages(target_language=target)

    for language in results:
        print("{name} ({language})".format(**language))

    return results


# [END translate_list_language_names]


# [START translate_text_with_model]
def translate_text_with_model(target: str, text: str, model: str = "nmt") -> dict:
    """Translates text into the target language.

    Make sure your project is allowlisted.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target, model=model)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result


# [END translate_text_with_model]


# [START translate_translate_text]
def translate_text(
    text: str | bytes | list[str] = "¡Hola amigos y amigas!",
    target_language: str = "en",
    source_language: str | None = None,
) -> dict:
    """Translates a given text into the specified target language.

    Find a list of supported languages and codes here:
    https://cloud.google.com/translate/docs/languages#nmt

    Args:
        text: The text to translate. Can be a string, bytes or a list of strings.
              If bytes, it will be decoded as UTF-8.
        target_language: The ISO 639 language code to translate the text into
                         (e.g., 'en' for English, 'es' for Spanish).
        source_language: Optional. The ISO 639 language code of the input text
                         (e.g., 'fr' for French). If None, the API will attempt
                         to detect the source language automatically.

    Returns:
        A dictionary containing the translation results.
    """

    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = [text.decode("utf-8")]

    if isinstance(text, str):
        text = [text]

    # If a string is supplied, a single dictionary will be returned.
    # In case a list of strings is supplied, this method
    # will return a list of dictionaries.

    # Find more information about translate function here:
    # https://cloud.google.com/python/docs/reference/translate/latest/google.cloud.translate_v2.client.Client#google_cloud_translate_v2_client_Client_translate
    results = translate_client.translate(
        values=text,
        target_language=target_language,
        source_language=source_language
    )

    for result in results:
        if "detectedSourceLanguage" in result:
            print(f"Detected source language: {result['detectedSourceLanguage']}")

        print(f"Input text: {result['input']}")
        print(f"Translated text: {result['translatedText']}")
        print()

    return results
# [END translate_translate_text]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    detect_langage_parser = subparsers.add_parser(
        "detect-language", help=detect_language.__doc__
    )
    detect_langage_parser.add_argument("text")

    list_languages_parser = subparsers.add_parser(
        "list-languages", help=list_languages.__doc__
    )

    list_languages_with_target_parser = subparsers.add_parser(
        "list-languages-with-target", help=list_languages_with_target.__doc__
    )
    list_languages_with_target_parser.add_argument("target")

    translate_text_parser = subparsers.add_parser(
        "translate-text", help=translate_text.__doc__
    )
    translate_text_parser.add_argument("target")
    translate_text_parser.add_argument("text")

    args = parser.parse_args()

    if args.command == "detect-language":
        detect_language(args.text)
    elif args.command == "list-languages":
        list_languages()
    elif args.command == "list-languages-with-target":
        list_languages_with_target(args.target)
    elif args.command == "translate-text":
        translate_text(text=args.text, target_language=args.target)

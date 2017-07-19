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
Google Cloud Natural Language API

For more information, the documentation at
https://cloud.google.com/natural-language/docs.
"""

import argparse

from google.cloud import language
from google.cloud.language import types
import six

# part-of-speech tags from google.cloud.language.enums.PartOfSpeech.Tag
POS_TAG = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
           'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')


# [START def_sentiment_text]
def sentiment_text(text):
    """Detects sentiment in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(content=text, type='PLAIN_TEXT')

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))
# [END def_sentiment_text]


# [START def_sentiment_file]
def sentiment_file(gcs_uri):
    """Detects sentiment in the file located in Google Cloud Storage."""
    client = language.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(gcs_content_uri=gcs_uri, type='PLAIN_TEXT')

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))
# [END def_sentiment_file]


# [START def_entities_text]
def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(content=text, type='PLAIN_TEXT')

    # Detects entities in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    entities = client.analyze_entities(document).entities

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity.type))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
# [END def_entities_text]


# [START def_entities_file]
def entities_file(gcs_uri):
    """Detects entities in the file located in Google Cloud Storage."""
    client = language.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(gcs_content_uri=gcs_uri, type='PLAIN_TEXT')

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    entities = client.analyze_entities(document).entities

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity.type))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
# [END def_entities_file]


# [START def_syntax_text]
def syntax_text(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(content=text, type='PLAIN_TEXT')

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    tokens = client.analyze_syntax(document).tokens

    for token in tokens:
        print(u'{}: {}'.format(POS_TAG[token.part_of_speech.tag],
                               token.text.content))
# [END def_syntax_text]


# [START def_syntax_file]
def syntax_file(gcs_uri):
    """Detects syntax in the file located in Google Cloud Storage."""
    client = language.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(gcs_content_uri=gcs_uri, type='PLAIN_TEXT')

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    tokens = client.analyze_syntax(document).tokens

    for token in tokens:
        print(u'{}: {}'.format(POS_TAG[token.part_of_speech.tag],
                               token.text.content))
# [END def_syntax_file]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    sentiment_text_parser = subparsers.add_parser(
        'sentiment-text', help=sentiment_text.__doc__)
    sentiment_text_parser.add_argument('text')

    sentiment_file_parser = subparsers.add_parser(
        'sentiment-file', help=sentiment_file.__doc__)
    sentiment_file_parser.add_argument('gcs_uri')

    entities_text_parser = subparsers.add_parser(
        'entities-text', help=entities_text.__doc__)
    entities_text_parser.add_argument('text')

    entities_file_parser = subparsers.add_parser(
        'entities-file', help=entities_file.__doc__)
    entities_file_parser.add_argument('gcs_uri')

    syntax_text_parser = subparsers.add_parser(
        'syntax-text', help=syntax_text.__doc__)
    syntax_text_parser.add_argument('text')

    syntax_file_parser = subparsers.add_parser(
        'syntax-file', help=syntax_file.__doc__)
    syntax_file_parser.add_argument('gcs_uri')

    args = parser.parse_args()

    if args.command == 'sentiment-text':
        sentiment_text(args.text)
    elif args.command == 'sentiment-file':
        sentiment_file(args.gcs_uri)
    elif args.command == 'entities-text':
        entities_text(args.text)
    elif args.command == 'entities-file':
        entities_file(args.gcs_uri)
    elif args.command == 'syntax-text':
        syntax_text(args.text)
    elif args.command == 'syntax-file':
        syntax_file(args.gcs_uri)

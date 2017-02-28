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


def sentiment_text(text):
    """Detects sentiment in the text."""
    language_client = language.Client()

    # Instantiates a plain text document.
    document = language_client.document_from_text(text)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    sentiment = document.analyze_sentiment().sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))


def sentiment_file(gcs_uri):
    """Detects sentiment in the file located in Google Cloud Storage."""
    language_client = language.Client()

    # Instantiates a plain text document.
    document = language_client.document_from_url(gcs_uri)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    sentiment = document.analyze_sentiment().sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))


def entities_text(text):
    """Detects entities in the text."""
    language_client = language.Client()

    # Instantiates a plain text document.
    document = language_client.document_from_text(text)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    entities = document.analyze_entities().entities

    for entity in entities:
        print('=' * 20)
        print('{:<16}: {}'.format('name', entity.name))
        print('{:<16}: {}'.format('type', entity.entity_type))
        print('{:<16}: {}'.format('metadata', entity.metadata))
        print('{:<16}: {}'.format('salience', entity.salience))
        print('{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))


def entities_file(gcs_uri):
    """Detects entities in the file located in Google Cloud Storage."""
    language_client = language.Client()

    # Instantiates a plain text document.
    document = language_client.document_from_url(gcs_uri)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    entities = document.analyze_entities().entities

    for entity in entities:
        print('=' * 20)
        print('{:<16}: {}'.format('name', entity.name))
        print('{:<16}: {}'.format('type', entity.entity_type))
        print('{:<16}: {}'.format('metadata', entity.metadata))
        print('{:<16}: {}'.format('salience', entity.salience))
        print('{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))


def syntax_text(text):
    """Detects syntax in the text."""
    language_client = language.Client()

    # Instantiates a plain text document.
    document = language_client.document_from_text(text)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    tokens = document.analyze_syntax().tokens

    for token in tokens:
        print('{}: {}'.format(token.part_of_speech, token.text_content))


def syntax_file(gcs_uri):
    """Detects syntax in the file located in Google Cloud Storage."""
    language_client = language.Client()

    # Instantiates a plain text document.
    document = language_client.document_from_url(gcs_uri)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.doc_type == language.Document.HTML
    tokens = document.analyze_syntax().tokens

    for token in tokens:
        print('{}: {}'.format(token.part_of_speech, token.text_content))


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

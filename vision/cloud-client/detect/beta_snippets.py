#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates beta features using the Google Cloud Vision API.

Example usage:
  python beta_snippets.py web-entities resources/city.jpg
  python beta_snippets.py detect-document resources/text.jpg
  python beta_snippets.py safe-search resources/wakeupcat.jpg
  python beta_snippets.py web-detect resources/landmark.jpg
"""

# [START imports]
import argparse
import io

from google.cloud import vision_v1p1beta1 as vision
# [END imports]


# [START vision_detect_document]
def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
                print(u'Paragraph Confidence: {}\n'.format(
                    paragraph.confidence))

            block_text = ''
            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
                word_text = ''
                for symbol in word.symbols:
                    word_text = word_text + symbol.text
                    print(u'\tSymbol text: {} (confidence: {})'.format(
                        symbol.text, symbol.confidence))
                print(u'Word text: {} (confidence: {})\n'.format(
                    word_text, word.confidence))

                block_text += ' ' + word_text

            print(u'Block Content: {}\n'.format(block_text))
            print(u'Block Confidence:\n {}\n'.format(block.confidence))
# [END vision_detect_document]


# [START vision_detect_document_uri]
def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
                print(u'Paragraph Confidence: {}\n'.format(
                    paragraph.confidence))

            block_text = ''
            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
                word_text = ''
                for symbol in word.symbols:
                    word_text = word_text + symbol.text
                    print(u'\tSymbol text: {} (confidence: {})'.format(
                        symbol.text, symbol.confidence))
                print(u'Word text: {} (confidence: {})\n'.format(
                    word_text, word.confidence))

                block_text += ' ' + word_text

            print(u'Block Content: {}\n'.format(block_text))
            print(u'Block Confidence:\n {}\n'.format(block.confidence))
# [END vision_detect_document_uri]


# [START vision_detect_safe_search]
def detect_safe_search(path):
    """Detects unsafe features in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
    print('racy: {}'.format(likelihood_name[safe.racy]))
# [END vision_detect_safe_search]


# [START vision_detect_safe_search_uri]
def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
    print('racy: {}'.format(likelihood_name[safe.racy]))
# [END vision_detect_safe_search_uri]


# [START vision_detect_web]
def detect_web(path):
    """Detects web annotations given an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))

    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))

            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))

                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))
# [END vision_detect_web]


# [START vision_detect_web_uri]
def detect_web_uri(uri):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))

    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))

            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))

                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))
# [END vision_detect_web_uri]


def web_entities(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.web_detection(image=image)

    for entity in response.web_detection.web_entities:
        print('\n\tScore      : {}'.format(entity.score))
        print(u'\tDescription: {}'.format(entity.description))


# [START vision_web_entities_include_geo_results]
def web_entities_include_geo_results(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    web_detection_params = vision.types.WebDetectionParams(
        include_geo_results=True)
    image_context = vision.types.ImageContext(
        web_detection_params=web_detection_params)

    response = client.web_detection(image=image, image_context=image_context)

    for entity in response.web_detection.web_entities:
        print('\n\tScore      : {}'.format(entity.score))
        print(u'\tDescription: {}'.format(entity.description))
# [END vision_web_entities_include_geo_results]


# [START vision_web_entities_include_geo_results_uri]
def web_entities_include_geo_results_uri(uri):
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image()
    image.source.image_uri = uri

    web_detection_params = vision.types.WebDetectionParams(
        include_geo_results=True)
    image_context = vision.types.ImageContext(
        web_detection_params=web_detection_params)

    response = client.web_detection(image=image, image_context=image_context)

    for entity in response.web_detection.web_entities:
        print('\n\tScore      : {}'.format(entity.score))
        print(u'\tDescription: {}'.format(entity.description))
# [END vision_web_entities_include_geo_results_uri]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    web_entities_parser = subparsers.add_parser(
        'web-entities')
    web_entities_parser.add_argument('path')

    web_entities_uri_parser = subparsers.add_parser(
        'web-entities-uri')
    web_entities_uri_parser.add_argument('uri')

    detect_document_parser = subparsers.add_parser(
        'detect-document')
    detect_document_parser.add_argument('path')

    detect_document_uri_parser = subparsers.add_parser(
        'detect-document-uri')
    detect_document_uri_parser.add_argument('uri')

    safe_search_parser = subparsers.add_parser(
        'safe-search')
    safe_search_parser.add_argument('path')

    safe_search_uri_parser = subparsers.add_parser(
        'safe-search-uri')
    safe_search_uri_parser.add_argument('uri')

    web_detect_parser = subparsers.add_parser(
        'web-detect')
    web_detect_parser.add_argument('path')

    web_detect_uri_parser = subparsers.add_parser(
        'web-detect-uri')
    web_detect_uri_parser.add_argument('uri')

    args = parser.parse_args()

    if args.command == 'web-entities':
        web_entities_include_geo_results(args.path)
    elif args.command == 'web-entities-uri':
        web_entities_include_geo_results_uri(args.uri)
    elif args.command == 'detect-document':
        detect_document(args.path)
    elif args.command == 'detect-document-uri':
        detect_document_uri(args.uri)
    elif args.command == 'safe-search':
        detect_safe_search(args.path)
    elif args.command == 'safe-search-uri':
        detect_safe_search_uri(args.uri)
    elif args.command == 'web-detect':
        detect_web(args.path)
    elif args.command == 'web-detect-uri':
        detect_web(args.uri)

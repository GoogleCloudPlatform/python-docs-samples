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

"""This application demonstrates how to perform basic operations with the
Google Cloud Vision API.

Example Usage:
python detect.py text ./resources/wakeupcat.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py web ./resources/landmark.jpg
python detect.py web-uri http://wheresgus.com/dog.JPG
python detect.py faces-uri gs://your-bucket/file.jpg

For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io

from google.cloud import vision
from google.cloud.vision import types


# [START def_detect_faces]
def detect_faces(path):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
    # [END migration_face_detection]
# [END def_detect_faces]


# [START def_detect_faces_uri]
def detect_faces_uri(uri):
    """Detects faces in the file located in Google Cloud Storage or the web."""
    client = vision.ImageAnnotatorClient()
    # [START migration_image_uri]
    image = types.Image()
    image.source.image_uri = uri
    # [END migration_image_uri]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
# [END def_detect_faces_uri]


# [START def_detect_labels]
def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)
    # [END migration_label_detection]
# [END def_detect_labels]


# [START def_detect_labels_uri]
def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)
# [END def_detect_labels_uri]


# [START def_detect_landmarks]
def detect_landmarks(path):
    """Detects landmarks in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_landmark_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude'.format(lat_lng.latitude))
            print('Longitude'.format(lat_lng.longitude))
    # [END migration_landmark_detection]
# [END def_detect_landmarks]


# [START def_detect_landmarks_uri]
def detect_landmarks_uri(uri):
    """Detects landmarks in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
# [END def_detect_landmarks_uri]


# [START def_detect_logos]
def detect_logos(path):
    """Detects logos in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_logo_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)
    # [END migration_logo_detection]
# [END def_detect_logos]


# [START def_detect_logos_uri]
def detect_logos_uri(uri):
    """Detects logos in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)
# [END def_detect_logos_uri]


# [START def_detect_safe_search]
def detect_safe_search(path):
    """Detects unsafe features in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_safe_search_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

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
    # [END migration_safe_search_detection]
# [END def_detect_safe_search]


# [START def_detect_safe_search_uri]
def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
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
# [END def_detect_safe_search_uri]


# [START def_detect_text]
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    # [END migration_text_detection]
# [END def_detect_text]


# [START def_detect_text_uri]
def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
# [END def_detect_text_uri]


# [START def_detect_properties]
def detect_properties(path):
    """Detects image properties in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_image_properties]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
    # [END migration_image_properties]
# [END def_detect_properties]


# [START def_detect_properties_uri]
def detect_properties_uri(uri):
    """Detects image properties in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('frac: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
# [END def_detect_properties_uri]


# [START def_detect_web]
def detect_web(path):
    """Detects web annotations given an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_web_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.web_detection(image=image)
    notes = response.web_detection

    if notes.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved')

        for page in notes.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if notes.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.web_entities:
        print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
    # [END migration_web_detection]
# [END def_detect_web]


# [START def_detect_web_uri]
def detect_web_uri(uri):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    notes = response.web_detection

    if notes.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved')

        for page in notes.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if notes.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.web_entities:
        print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
# [END def_detect_web_uri]


# [START def_detect_crop_hints]
def detect_crop_hints(path):
    """Detects crop hints in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_crop_hints]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    # [END migration_crop_hints]
# [END def_detect_crop_hints]


# [START def_detect_crop_hints_uri]
def detect_crop_hints_uri(uri):
    """Detects crop hints in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
# [END def_detect_crop_hints_uri]


# [START def_detect_document]
def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_document_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))
    # [END migration_document_text_detection]
# [END def_detect_document]


# [START def_detect_document_uri]
def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))
# [END def_detect_document_uri]


def run_local(args):
    if args.command == 'faces':
        detect_faces(args.path)
    elif args.command == 'labels':
        detect_labels(args.path)
    elif args.command == 'landmarks':
        detect_landmarks(args.path)
    elif args.command == 'text':
        detect_text(args.path)
    elif args.command == 'logos':
        detect_logos(args.path)
    elif args.command == 'safe-search':
        detect_safe_search(args.path)
    elif args.command == 'properties':
        detect_properties(args.path)
    elif args.command == 'web':
        detect_web(args.path)
    elif args.command == 'crophints':
        detect_crop_hints(args.path)
    elif args.command == 'document':
        detect_document(args.path)


def run_uri(args):
    if args.command == 'text-uri':
        detect_text_uri(args.uri)
    elif args.command == 'faces-uri':
        detect_faces_uri(args.uri)
    elif args.command == 'labels-uri':
        detect_labels_uri(args.uri)
    elif args.command == 'landmarks-uri':
        detect_landmarks_uri(args.uri)
    elif args.command == 'logos-uri':
        detect_logos_uri(args.uri)
    elif args.command == 'safe-search-uri':
        detect_safe_search_uri(args.uri)
    elif args.command == 'properties-uri':
        detect_properties_uri(args.uri)
    elif args.command == 'web-uri':
        detect_web_uri(args.uri)
    elif args.command == 'crophints-uri':
        detect_crop_hints_uri(args.uri)
    elif args.command == 'document-uri':
        detect_document_uri(args.uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    detect_faces_parser = subparsers.add_parser(
        'faces', help=detect_faces.__doc__)
    detect_faces_parser.add_argument('path')

    faces_file_parser = subparsers.add_parser(
        'faces-uri', help=detect_faces_uri.__doc__)
    faces_file_parser.add_argument('uri')

    detect_labels_parser = subparsers.add_parser(
        'labels', help=detect_labels.__doc__)
    detect_labels_parser.add_argument('path')

    labels_file_parser = subparsers.add_parser(
        'labels-uri', help=detect_labels_uri.__doc__)
    labels_file_parser.add_argument('uri')

    detect_landmarks_parser = subparsers.add_parser(
        'landmarks', help=detect_landmarks.__doc__)
    detect_landmarks_parser.add_argument('path')

    landmark_file_parser = subparsers.add_parser(
        'landmarks-uri', help=detect_landmarks_uri.__doc__)
    landmark_file_parser.add_argument('uri')

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    detect_text_parser.add_argument('path')

    text_file_parser = subparsers.add_parser(
        'text-uri', help=detect_text_uri.__doc__)
    text_file_parser.add_argument('uri')

    detect_logos_parser = subparsers.add_parser(
        'logos', help=detect_logos.__doc__)
    detect_logos_parser.add_argument('path')

    logos_file_parser = subparsers.add_parser(
        'logos-uri', help=detect_logos_uri.__doc__)
    logos_file_parser.add_argument('uri')

    safe_search_parser = subparsers.add_parser(
        'safe-search', help=detect_safe_search.__doc__)
    safe_search_parser.add_argument('path')

    safe_search_file_parser = subparsers.add_parser(
        'safe-search-uri',
        help=detect_safe_search_uri.__doc__)
    safe_search_file_parser.add_argument('uri')

    properties_parser = subparsers.add_parser(
        'properties', help=detect_properties.__doc__)
    properties_parser.add_argument('path')

    properties_file_parser = subparsers.add_parser(
        'properties-uri',
        help=detect_properties_uri.__doc__)
    properties_file_parser.add_argument('uri')

    # 1.1 Vision features
    web_parser = subparsers.add_parser(
        'web', help=detect_web.__doc__)
    web_parser.add_argument('path')

    web_uri_parser = subparsers.add_parser(
        'web-uri',
        help=detect_web_uri.__doc__)
    web_uri_parser.add_argument('uri')

    crop_hints_parser = subparsers.add_parser(
        'crophints', help=detect_crop_hints.__doc__)
    crop_hints_parser.add_argument('path')

    crop_hints_uri_parser = subparsers.add_parser(
        'crophints-uri', help=detect_crop_hints_uri.__doc__)
    crop_hints_uri_parser.add_argument('uri')

    document_parser = subparsers.add_parser(
        'document', help=detect_document.__doc__)
    document_parser.add_argument('path')

    document_uri_parser = subparsers.add_parser(
        'document-uri', help=detect_document_uri.__doc__)
    document_uri_parser.add_argument('uri')

    args = parser.parse_args()

    if ('uri' in args.command):
        run_uri(args)
    else:
        run_local(args)

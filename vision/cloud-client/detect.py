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

For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io
import os

from google.cloud import vision


def detect_faces(path):
    """Detects faces in an image."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    faces = image.detect_faces()

    print('Faces:')
    for face in faces:
        print('anger: {}'.format(face.emotions.anger))
        print('joy: {}'.format(face.emotions.joy))
        print('surprise: {}'.format(face.emotions.surprise))


def detect_faces_cloud_storage(uri):
    """Detects faces in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    faces = image.detect_faces()

    print('Faces:')
    for face in faces:
        print('anger: {}'.format(face.emotions.anger))
        print('joy: {}'.format(face.emotions.joy))
        print('surprise: {}'.format(face.emotions.surprise))


def detect_labels(path):
    """Detects labels in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    labels = image.detect_labels()

    print('Labels:')
    for label in labels:
        print(label.description)


def detect_labels_cloud_storage(uri):
    """Detects labels in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    labels = image.detect_labels()

    print('Labels:')
    for label in labels:
        print(label.description)


def detect_landmarks(path):
    """Detects landmarks in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    landmarks = image.detect_landmarks()

    print('Landmarks:')
    for landmark in landmarks:
        print(landmark.description)


def detect_landmarks_cloud_storage(uri):
    """Detects landmarks in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    landmarks = image.detect_landmarks()

    print('Landmarks:')
    for landmark in landmarks:
        print(landmark.description)


def detect_logos(path):
    """Detects logos in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    logos = image.detect_logos()

    print('Logos:')
    for logo in logos:
        print(logo.description)


def detect_logos_cloud_storage(uri):
    """Detects logos in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    logos = image.detect_logos()

    print('Logos:')
    for logo in logos:
        print(logo.description)


def detect_safe_search(path):
    """Detects unsafe features in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    safe_searches = image.detect_safe_search()
    print('Safe search:')
    for safe in safe_searches:
        print('adult: {}'.format(safe.adult))
        print('medical: {}'.format(safe.medical))
        print('spoofed: {}'.format(safe.spoof))
        print('violence: {}'.format(safe.violence))


def detect_safe_search_cloud_storage(uri):
    """Detects unsafe features in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    safe_searches = image.detect_safe_search()
    print('Safe search:')
    for safe in safe_searches:
        print('adult: {}'.format(safe.adult))
        print('medical: {}'.format(safe.medical))
        print('spoofed: {}'.format(safe.spoof))
        print('violence: {}'.format(safe.violence))


def detect_text(path):
    """Detects text in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    texts = image.detect_text()
    print('Texts:')
    for text in texts:
        print(text.description)


def detect_text_cloud_storage(uri):
    """Detects text in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    texts = image.detect_text()
    print('Texts:')
    for text in texts:
        print(text.description)


def detect_properties(path):
    """Detects image properties in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    properties = image.detect_properties()
    print('Properties:')
    for prop in properties:
        color = prop.colors[0]
        print('fraction: {}'.format(color.pixel_fraction))
        print('r: {}'.format(color.color.red))
        print('g: {}'.format(color.color.green))
        print('b: {}'.format(color.color.blue))


def detect_properties_cloud_storage(uri):
    """Detects image properties in the file located in Google Cloud Storage."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    properties = image.detect_properties()
    for prop in properties:
        color = prop.colors[0]
        print('fraction: {}'.format(color.pixel_fraction))
        print('r: {}'.format(color.color.red))
        print('g: {}'.format(color.color.green))
        print('g: {}'.format(color.color.blue))


def run_all_local():
    """Runs all available detection operations on the local resources."""
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect_labels(file_name)

    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect_landmarks(file_name)

    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/face_no_surprise.jpg')
    detect_faces(file_name)

    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/logos.png')
    detect_logos(file_name)

    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect_safe_search(file_name)

    ''' TODO: Uncomment when https://goo.gl/c47YwV is fixed
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    detect_text(file_name)
    '''

    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect_properties(file_name)


def run_local(args):
    if args.command == 'all-local':
        run_all_local()
    elif args.command == 'faces':
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


def run_cloud_storage(args):
    if args.command == 'text-gcs':
        detect_text_cloud_storage(args.cloud_storage_uri)
    elif args.command == 'faces-gcs':
        detect_faces_cloud_storage(args.cloud_storage_uri)
    elif args.command == 'labels-gcs':
        detect_labels_cloud_storage(args.cloud_storage_uri)
    elif args.command == 'landmarks-gcs':
        detect_landmarks_cloud_storage(args.cloud_storage_uri)
    elif args.command == 'logos-gcs':
        detect_logos_cloud_storage(args.cloud_storage_uri)
    elif args.command == 'safe-search-gcs':
        detect_safe_search_cloud_storage(args.cloud_storage_uri)
    elif args.command == 'properties-gcs':
        detect_properties_cloud_storage(args.cloud_storage_uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    run_local_parser = subparsers.add_parser(
        'all-local', help=run_all_local.__doc__)

    detect_faces_parser = subparsers.add_parser(
        'faces', help=detect_faces.__doc__)
    detect_faces_parser.add_argument('path')

    faces_file_parser = subparsers.add_parser(
        'faces-gcs', help=detect_faces_cloud_storage.__doc__)
    faces_file_parser.add_argument('cloud_storage_uri')

    detect_labels_parser = subparsers.add_parser(
        'labels', help=detect_labels.__doc__)
    detect_labels_parser.add_argument('path')

    labels_file_parser = subparsers.add_parser(
        'labels-gcs', help=detect_labels_cloud_storage.__doc__)
    labels_file_parser.add_argument('cloud_storage_uri')

    detect_landmarks_parser = subparsers.add_parser(
        'landmarks', help=detect_landmarks.__doc__)
    detect_landmarks_parser.add_argument('path')

    landmark_file_parser = subparsers.add_parser(
        'landmarks-gcs', help=detect_landmarks_cloud_storage.__doc__)
    landmark_file_parser.add_argument('cloud_storage_uri')

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    detect_text_parser.add_argument('path')

    text_file_parser = subparsers.add_parser(
        'text-gcs', help=detect_text_cloud_storage.__doc__)
    text_file_parser.add_argument('cloud_storage_uri')

    detect_logos_parser = subparsers.add_parser(
        'logos', help=detect_logos.__doc__)
    detect_logos_parser.add_argument('path')

    logos_file_parser = subparsers.add_parser(
        'logos-gcs', help=detect_logos_cloud_storage.__doc__)
    logos_file_parser.add_argument('cloud_storage_uri')

    safe_search_parser = subparsers.add_parser(
        'safe-search', help=detect_safe_search.__doc__)
    safe_search_parser.add_argument('path')

    safe_search_file_parser = subparsers.add_parser(
        'safe-search-gcs',
        help=detect_safe_search_cloud_storage.__doc__)
    safe_search_file_parser.add_argument('cloud_storage_uri')

    properties_parser = subparsers.add_parser(
        'properties', help=detect_safe_search.__doc__)
    properties_parser.add_argument('path')

    properties_file_parser = subparsers.add_parser(
        'properties-gcs',
        help=detect_properties_cloud_storage.__doc__)
    properties_file_parser.add_argument('cloud_storage_uri')

    args = parser.parse_args()

    if ('gcs' in args.command):
        run_cloud_storage(args)
    else:
        run_local(args)

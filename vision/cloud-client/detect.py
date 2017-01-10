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

# Imports the Google Cloud client library
from google.cloud import vision


def detect_faces(path):
    """Detects faces in an image."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs face detection on the image file
    faces = image.detect_faces()

    print 'Faces:'
    for face in faces:
        print 'anger', face.emotions.anger
        print 'joy', face.emotions.joy
        print 'surprise', face.emotions.surprise
    print


def detect_faces_gcs(path):
    """Detects faces in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs face detection on the image file
    faces = image.detect_faces()

    print 'Faces:'
    for face in faces:
        print 'anger', face.emotions.anger
        print 'joy', face.emotions.joy
        print 'surprise', face.emotions.surprise
    print


def detect_labels(path):
    """Detects labels in the file."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    labels = image.detect_labels()

    print 'Labels:'
    for label in labels:
        print label.description
    print


def detect_labels_gcs(path):
    """Detects labels in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs label detection on the image file
    labels = image.detect_labels()

    print 'Labels:'
    for label in labels:
        print label.description
    print


def detect_landmarks(path):
    """Detects landmarks in the file."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    landmarks = image.detect_landmarks()

    print 'Landmarks:'
    for landmark in landmarks:
        print landmark.description
    print


def detect_landmarks_gcs(path):
    """Detects landmarks in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs label detection on the image file
    landmarks = image.detect_landmarks()

    print 'Landmarks:'
    for landmark in landmarks:
        print landmark.description
    print


def detect_logos(path):
    """Detects logos in the file."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)

    # Performs label detection on the image file
    logos = image.detect_logos()

    print 'Logos:'
    for logo in logos:
        print logo.description
    print


def detect_logos_gcs(path):
    """Detects logos in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs label detection on the image file
    logos = image.detect_logos()

    print 'Logos:'
    for logo in logos:
        print logo.description
    print


def detect_safe_search(path):
    """Detects unsafe features in the file."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    safe_searches = image.detect_safe_search()
    print 'Safe search:'
    for safe in safe_searches:
        print 'adult', safe.adult
        print 'medical', safe.medical
        print 'spoofed', safe.spoof
        print 'violence', safe.violence
    print


def detect_safe_search_gcs(path):
    """Detects unsafe features in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs label detection on the image file
    safe_searches = image.detect_safe_search()
    print 'Safe search:'
    for safe in safe_searches:
        print 'adult', safe.adult
        print 'medical', safe.medical
        print 'spoofed', safe.spoof
        print 'violence', safe.violence
    print


def detect_text(path):
    """Detects text in the file."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    texts = image.detect_text()
    print 'Texts:'
    for text in texts:
        print text.description
    print


def detect_text_gcs(path):
    """Detects text in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs label detection on the image file
    texts = image.detect_text()
    print 'Texts:'
    for text in texts:
        print text.description
    print


def detect_properties(path):
    """Detects image properties in the file."""
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    properties = image.detect_properties()
    print 'Properties:'
    for prop in properties:
        color = prop.colors[0]
        print 'fraction: ', color.pixel_fraction
        print 'r: ', color.color.red
        print 'g: ', color.color.green
        print 'b: ', color.color.blue
    print


def detect_properties_gcs(path):
    """Detects image properties in the file located in Google Cloud Storage."""
    # Instantiates a client
    vision_client = vision.Client()
    image = vision_client.image(source_uri=path)

    # Performs label detection on the image file
    properties = image.detect_properties()
    print 'Properties:'
    for prop in properties:
        color = prop.colors[0]
        print 'fraction: ', color.pixel_fraction
        print 'r: ', color.color.red
        print 'g: ', color.color.green
        print 'b: ', color.color.blue
    print


def run_all_local():
    """Runs all available detection operations on the local resources."""
    # Detect labels from local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect_labels(file_name)

    # Detect a landmark in local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect_landmarks(file_name)

    # Detect a face in local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/face_no_surprise.jpg')
    detect_faces(file_name)

    # Detect a logo in local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/logos.png')
    detect_logos(file_name)

    # Detect safe search in local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect_safe_search(file_name)

    # Detect text in local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    detect_text(file_name)

    # Detect properties in local file
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect_properties(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    run_local_parser = subparsers.add_parser(
        'local', help=run_all_local.__doc__)

    detect_faces_parser = subparsers.add_parser(
        'faces', help=detect_faces.__doc__)
    detect_faces_parser.add_argument('path')

    faces_file_parser = subparsers.add_parser(
        'faces-gcs', help=detect_faces_gcs.__doc__)
    faces_file_parser.add_argument('gcs_uri')

    detect_labels_parser = subparsers.add_parser(
        'labels', help=detect_labels.__doc__)
    detect_labels_parser.add_argument('path')

    labels_file_parser = subparsers.add_parser(
        'labels-gcs', help=detect_labels_gcs.__doc__)
    labels_file_parser.add_argument('gcs_uri')

    detect_landmarks_parser = subparsers.add_parser(
        'landmarks', help=detect_landmarks.__doc__)
    detect_landmarks_parser.add_argument('path')

    landmark_file_parser = subparsers.add_parser(
        'landmarks-gcs', help=detect_landmarks_gcs.__doc__)
    landmark_file_parser.add_argument('gcs_uri')

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    detect_text_parser.add_argument('path')

    text_file_parser = subparsers.add_parser(
        'text-gcs', help=detect_text_gcs.__doc__)
    text_file_parser.add_argument('gcs_uri')

    detect_logos_parser = subparsers.add_parser(
        'logos', help=detect_logos.__doc__)
    detect_logos_parser.add_argument('path')

    logos_file_parser = subparsers.add_parser(
        'logos-gcs', help=detect_logos_gcs.__doc__)
    logos_file_parser.add_argument('gcs_uri')

    safe_search_parser = subparsers.add_parser(
        'safe-search', help=detect_safe_search.__doc__)
    safe_search_parser.add_argument('path')

    safe_search_file_parser = subparsers.add_parser(
        'safe-search-gcs', help=detect_safe_search_gcs.__doc__)
    safe_search_file_parser.add_argument('gcs_uri')

    properties_parser = subparsers.add_parser(
        'properties', help=detect_safe_search.__doc__)
    properties_parser.add_argument('path')

    properties_file_parser = subparsers.add_parser(
        'properties-gcs', help=detect_properties_gcs.__doc__)
    properties_file_parser.add_argument('gcs_uri')

    args = parser.parse_args()

    if args.command == 'local':
        run_all_local()
    elif args.command == 'faces':
        detect_faces(args.path)
    elif args.command == 'faces-gcs':
        detect_faces_gcs(args.gcs_uri)
    elif args.command == 'labels':
        detect_labels(args.path)
    elif args.command == 'labels-gcs':
        detect_labels_gcs(args.gcs_uri)
    elif args.command == 'landmarks':
        detect_landmarks(args.path)
    elif args.command == 'landmarks-gcs':
        detect_landmarks_gcs(args.gcs_uri)
    elif args.command == 'text':
        detect_text(args.path)
    elif args.command == 'text-gcs':
        detect_text_gcs(args.gcs_uri)
    elif args.command == 'logos':
        detect_logos(args.path)
    elif args.command == 'logos-gcs':
        detect_logos_gcs(args.gcs_uri)
    elif args.command == 'safe-search':
        detect_safe_search(args.path)
    elif args.command == 'safe-search-gcs':
        detect_safe_search_gcs(args.gcs_uri)
    elif args.command == 'properties':
        detect_properties(args.path)
    elif args.command == 'properties-gcs':
        detect_properties_gcs(args.gcs_uri)

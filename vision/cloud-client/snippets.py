#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision


# [START face_detection]
def detect_faces(path):
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
# [END face_detection]


# [START label_detection]
def detect_labels(path):
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
# [END label_detection]


# [START landmark_detection]
def detect_landmarks(path):
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
# [END landmark_detection]


# [START logo_detection]
def detect_logos(path):
    # Instantiates a client
    vision_client = vision.Client()

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    logos = image.detect_logos()

    print 'Logos:'
    for logo in logos:
        print logo.description
    print
# [END logo_detection]


# [START safe_search_detection]
def detect_safe_search(path):
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
# [END safe_search_detection]


# [START text_detection]
def detect_text(path):
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
# [END text_detection]


# [START property_detection]
def detect_properties(path):
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
# [END property_detection]


def run_snippets():
    # Detect labels
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect_labels(file_name)

    # Detect a landmark
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect_landmarks(file_name)

    # Detect a face
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/face_no_surprise.jpg')
    detect_faces(file_name)

    # Detect a logo
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/logos.png')
    detect_logos(file_name)

    # Detect safe search
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect_safe_search(file_name)

    # Detect text
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    detect_text(file_name)

    # Detect properties
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect_properties(file_name)


if __name__ == '__main__':
    run_snippets()

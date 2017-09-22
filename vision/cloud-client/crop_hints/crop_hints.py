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

"""Outputs a cropped image or an image highlighting crop regions on an image.

Examples:
    python crop_hints.py resources/cropme.jpg draw
    python crop_hints.py resources/cropme.jpg crop
"""
# [START full_tutorial]
# [START imports]
import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
# [END imports]


def get_crop_hint(path):
    # [START get_crop_hint]
    """Detect crop hints on a single image and return the first result."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.77.
    vertices = hints[0].bounding_poly.vertices
    # [END get_crop_hint]

    return vertices


def draw_hint(image_file):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_hint]
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon([
        vects[0].x, vects[0].y,
        vects[1].x, vects[1].y,
        vects[2].x, vects[2].y,
        vects[3].x, vects[3].y], None, 'red')
    im.save('output-hint.jpg', 'JPEG')
    # [END draw_hint]


def crop_to_hint(image_file):
    """Crop the image using the hints in the vector list."""
    # [START crop_to_hint]
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y,
                  vects[2].x - 1, vects[2].y - 1])
    im2.save('output-crop.jpg', 'JPEG')
    # [END crop_to_hint]


if __name__ == '__main__':
    # [START run_crop]
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to crop.')
    parser.add_argument('mode', help='Set to "crop" or "draw".')
    args = parser.parse_args()

    parser = argparse.ArgumentParser()

    if args.mode == 'crop':
        crop_to_hint(args.image_file)
    elif args.mode == 'draw':
        draw_hint(args.image_file)
    # [END run_crop]
# [END full_tutorial]

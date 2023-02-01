#!/usr/bin/env python

# Copyright 2017 Google LLC
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
# [START vision_crop_hints_tutorial]
# [START vision_crop_hints_tutorial_imports]
import argparse
import io

from google.cloud import vision
from PIL import Image, ImageDraw
# [END vision_crop_hints_tutorial_imports]


def get_crop_hint(path):
    # [START vision_crop_hints_tutorial_get_crop_hints]
    """Detect crop hints on a single image and return the first result."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    crop_hints_params = vision.CropHintsParams(aspect_ratios=[1.77])
    image_context = vision.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.77.
    vertices = hints[0].bounding_poly.vertices
    # [END vision_crop_hints_tutorial_get_crop_hints]

    return vertices


def draw_hint(image_file):
    """Draw a border around the image using the hints in the vector list."""
    # [START vision_crop_hints_tutorial_draw_crop_hints]
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon([
        vects[0].x, vects[0].y,
        vects[1].x, vects[1].y,
        vects[2].x, vects[2].y,
        vects[3].x, vects[3].y], None, 'red')
    im.save('output-hint.jpg', 'JPEG')
    print('Saved new image to output-hint.jpg')
    # [END vision_crop_hints_tutorial_draw_crop_hints]


def crop_to_hint(image_file):
    """Crop the image using the hints in the vector list."""
    # [START vision_crop_hints_tutorial_crop_to_hints]
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y,
                  vects[2].x - 1, vects[2].y - 1])
    im2.save('output-crop.jpg', 'JPEG')
    print('Saved new image to output-crop.jpg')
    # [END vision_crop_hints_tutorial_crop_to_hints]


if __name__ == '__main__':
    # [START vision_crop_hints_tutorial_run_application]
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to crop.')
    parser.add_argument('mode', help='Set to "crop" or "draw".')
    args = parser.parse_args()

    if args.mode == 'crop':
        crop_to_hint(args.image_file)
    elif args.mode == 'draw':
        draw_hint(args.image_file)
    # [END vision_crop_hints_tutorial_run_application]
# [END vision_crop_hints_tutorial]

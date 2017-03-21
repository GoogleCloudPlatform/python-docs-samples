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

"""Outlines document text given an image.

Example:
    python doctext.py resources/cropme.jpg
"""
# [START full_tutorial]
# [START imports]
import argparse
from enum import Enum
import io

from google.cloud import vision
from PIL import Image, ImageDraw
# [END imports]


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(im, blocks, color, width):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(im)

    for block in blocks:
        draw.line([block.vertices[0].x, block.vertices[0].y,
                  block.vertices[1].x, block.vertices[1].y],
                  fill=color, width=width)
        draw.line([block.vertices[1].x, block.vertices[1].y,
                  block.vertices[2].x, block.vertices[2].y],
                  fill=color, width=width)
        draw.line([block.vertices[2].x, block.vertices[2].y,
                  block.vertices[3].x, block.vertices[3].y],
                  fill=color, width=width)
        draw.line([block.vertices[3].x, block.vertices[3].y,
                  block.vertices[0].x, block.vertices[0].y],
                  fill=color, width=width)

    return im
    # [END draw_blocks]


def get_document_bounds(image_file, feature):
    # [START detect_bounds]
    """Returns document bounds given an image."""
    vision_client = vision.Client()

    bounds = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)
    document = image.detect_full_text()

    for b, page in enumerate(document.pages):

        for bb, block in enumerate(page.blocks):

            for p, paragraph in enumerate(block.paragraphs):

                for w, word in enumerate(paragraph.words):

                    for s, symbol in enumerate(word.symbols):

                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    return bounds
    # [END detect_bounds]


def render_doc_text(filein, fileout):
    # [START render_doc_text]
    im = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.PAGE)
    draw_boxes(im, bounds, 'blue', 3)
    bounds = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(im, bounds, 'green', 2)
    bounds = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(im, bounds, 'yellow', 1)

    if fileout is not 0:
        im.save(fileout)
    else:
        im.show()
    # [END render_doc_text]


if __name__ == '__main__':
    # [START run_crop]
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    parser = argparse.ArgumentParser()
    render_doc_text(args.detect_file, args.out_file)

    # [END run_crop]
# [END full_tutorial]

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

"""Demonstrates web detection using the Google Cloud Vision API.

Example usage:
  python web_detect.py https://goo.gl/X4qcB6
  python web_detect.py ../detect/resources/landmark.jpg
  python web_detect.py gs://your-bucket/image.png
"""
# [START vision_web_detection_tutorial]
# [START vision_web_detection_tutorial_imports]
import argparse

from google.cloud import vision

# [END vision_web_detection_tutorial_imports]


def annotate(path: str) -> vision.WebDetection:
    """Returns web annotations given the path to an image.

    Args:
        path: path to the input image.

    Returns:
        An WebDetection object with relevant information of the
        image from the internet (i.e., the annotations).
    """
    # [START vision_web_detection_tutorial_annotate]
    client = vision.ImageAnnotatorClient()

    if path.startswith("http") or path.startswith("gs:"):
        image = vision.Image()
        image.source.image_uri = path

    else:
        with open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection
    # [END vision_web_detection_tutorial_annotate]

    return web_detection


def report(annotations: vision.WebDetection) -> None:
    """Prints detected features in the provided web annotations.

    Args:
        annotations: The web annotations (WebDetection object) from which
        the features should be parsed and printed.
    """
    # [START vision_web_detection_tutorial_print_annotations]
    if annotations.pages_with_matching_images:
        print(
            f"\n{len(annotations.pages_with_matching_images)} Pages with matching images retrieved"
        )

        for page in annotations.pages_with_matching_images:
            print(f"Url   : {page.url}")

    if annotations.full_matching_images:
        print(f"\n{len(annotations.full_matching_images)} Full Matches found: ")

        for image in annotations.full_matching_images:
            print(f"Url  : {image.url}")

    if annotations.partial_matching_images:
        print(f"\n{len(annotations.partial_matching_images)} Partial Matches found: ")

        for image in annotations.partial_matching_images:
            print(f"Url  : {image.url}")

    if annotations.web_entities:
        print(f"\n{len(annotations.web_entities)} Web entities found: ")

        for entity in annotations.web_entities:
            print(f"Score      : {entity.score}")
            print(f"Description: {entity.description}")
    # [END vision_web_detection_tutorial_print_annotations]


if __name__ == "__main__":
    # [START vision_web_detection_tutorial_run_application]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    path_help = str(
        "The image to detect, can be web URI, "
        "Google Cloud Storage, or path to local file."
    )
    parser.add_argument("image_url", help=path_help)
    args = parser.parse_args()

    report(annotate(args.image_url))
    # [END vision_web_detection_tutorial_run_application]
# [END vision_web_detection_tutorial]

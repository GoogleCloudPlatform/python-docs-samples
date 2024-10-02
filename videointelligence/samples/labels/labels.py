#!/usr/bin/env python

# Copyright 2017 Google LLC.
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

"""This application demonstrates how to detect labels from a video
based on the image content with the Google Cloud Video Intelligence
API.

For more information, check out the documentation at
https://cloud.google.com/videointelligence/docs.

Usage Example:

    python labels.py gs://cloud-ml-sandbox/video/chicago.mp4

"""

# [START video_label_tutorial]
# [START video_label_tutorial_imports]
import argparse

from google.cloud import videointelligence

# [END video_label_tutorial_imports]


def analyze_labels(path):
    """Detects labels given a GCS path."""
    # [START video_label_tutorial_construct_request]
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    # [END video_label_tutorial_construct_request]
    print("\nProcessing video for label annotations:")

    # [START video_label_tutorial_check_operation]
    result = operation.result(timeout=90)
    print("\nFinished processing.")
    # [END video_label_tutorial_check_operation]

    # [START video_label_tutorial_parse_response]
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print("Video label description: {}".format(segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, segment in enumerate(segment_label.segments):
            start_time = (
                segment.segment.start_time_offset.seconds
                + segment.segment.start_time_offset.microseconds / 1e6
            )
            end_time = (
                segment.segment.end_time_offset.seconds
                + segment.segment.end_time_offset.microseconds / 1e6
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = segment.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")
    # [END video_label_tutorial_parse_response]


if __name__ == "__main__":
    # [START video_label_tutorial_run_application]
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="GCS file path for label detection.")
    args = parser.parse_args()

    analyze_labels(args.path)
    # [END video_label_tutorial_run_application]
# [END video_label_tutorial]

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

"""This application demonstrates how to identify all different shots
in a video using the Google Cloud Video Intelligence API.

For more information, check out the documentation at
https://cloud.google.com/videointelligence/docs.

Example Usage:

    python shotchange.py gs://cloud-samples-data/video/gbikes_dinosaur.mp4

"""

# [START video_shot_tutorial]
# [START video_shot_tutorial_imports]
import argparse

from google.cloud import videointelligence

# [END video_shot_tutorial_imports]


def analyze_shots(path):
    """Detects camera shot changes."""
    # [START video_shot_tutorial_construct_request]
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    # [END video_shot_tutorial_construct_request]
    print("\nProcessing video for shot change annotations:")

    # [START video_shot_tutorial_check_operation]
    result = operation.result(timeout=120)
    print("\nFinished processing.")

    # [END video_shot_tutorial_check_operation]

    # [START video_shot_tutorial_parse_response]
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = (
            shot.start_time_offset.seconds + shot.start_time_offset.microseconds / 1e6
        )
        end_time = (
            shot.end_time_offset.seconds + shot.end_time_offset.microseconds / 1e6
        )
        print("\tShot {}: {} to {}".format(i, start_time, end_time))
    # [END video_shot_tutorial_parse_response]


if __name__ == "__main__":
    # [START video_shot_tutorial_run_application]
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="GCS path for shot change detection.")
    args = parser.parse_args()

    analyze_shots(args.path)
    # [END video_shot_tutorial_run_application]
# [END video_shot_tutorial]

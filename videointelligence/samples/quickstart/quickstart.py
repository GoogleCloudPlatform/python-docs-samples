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

"""This application demonstrates label detection using the Google Cloud API.

Usage:
    python quickstart.py
"""


def run_quickstart():
    # [START videointelligence_quickstart]
    import sys
    import time

    from google.cloud.gapic.videointelligence.v1beta1 import enums
    from google.cloud.gapic.videointelligence.v1beta1 import (
        video_intelligence_service_client)

    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video('gs://demomaker/cat.mp4', features)
    print('\nProcessing video for label annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    results = operation.result().annotation_results[0]

    for label in results.label_annotations:
        print('Label description: {}'.format(label.description))
        print('Locations:')

        for l, location in enumerate(label.locations):
            positions = 'Entire video'
            if (location.segment.start_time_offset != -1 or
                    location.segment.end_time_offset != -1):
                positions = '{} to {}'.format(
                    location.segment.start_time_offset / 1000000.0,
                    location.segment.end_time_offset / 1000000.0)
            print('\t{}: {}'.format(l, positions))

        print('\n')
    # [END videointelligence_quickstart]


if __name__ == '__main__':
    run_quickstart()

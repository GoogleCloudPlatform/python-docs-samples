#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Transcoder sample for creating a job template.

Example usage:
    python create_job_template.py --project_id <project-id> [--location <location>] [--template_id <template-id>]
"""

# [START transcoder_create_job_template]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)


def create_job_template(project_id, location, template_id):
    """Creates a job template.

    Args:
        project_id: The GCP project ID.
        location: The location to store this template in.
        template_id: The user-defined template ID."""

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    job_template = transcoder_v1.types.JobTemplate()
    job_template.name = (
        f"projects/{project_id}/locations/{location}/jobTemplates/{template_id}"
    )
    job_template.config = transcoder_v1.types.JobConfig(
        elementary_streams=[
            transcoder_v1.types.ElementaryStream(
                key="video-stream0",
                video_stream=transcoder_v1.types.VideoStream(
                    h264=transcoder_v1.types.VideoStream.H264CodecSettings(
                        height_pixels=360,
                        width_pixels=640,
                        bitrate_bps=550000,
                        frame_rate=60,
                    ),
                ),
            ),
            transcoder_v1.types.ElementaryStream(
                key="video-stream1",
                video_stream=transcoder_v1.types.VideoStream(
                    h264=transcoder_v1.types.VideoStream.H264CodecSettings(
                        height_pixels=720,
                        width_pixels=1280,
                        bitrate_bps=2500000,
                        frame_rate=60,
                    ),
                ),
            ),
            transcoder_v1.types.ElementaryStream(
                key="audio-stream0",
                audio_stream=transcoder_v1.types.AudioStream(
                    codec="aac", bitrate_bps=64000
                ),
            ),
        ],
        mux_streams=[
            transcoder_v1.types.MuxStream(
                key="sd",
                container="mp4",
                elementary_streams=["video-stream0", "audio-stream0"],
            ),
            transcoder_v1.types.MuxStream(
                key="hd",
                container="mp4",
                elementary_streams=["video-stream1", "audio-stream0"],
            ),
        ],
    )

    response = client.create_job_template(
        parent=parent, job_template=job_template, job_template_id=template_id
    )
    print(f"Job template: {response.name}")
    return response


# [END transcoder_create_job_template]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location to store this template in.",
        default="us-central1",
    )
    parser.add_argument(
        "--template_id", help="The job template ID.", default="my-job-template"
    )
    args = parser.parse_args()
    create_job_template(args.project_id, args.location, args.template_id)

#!/usr/bin/env python

# Copyright 2021 Google LLC
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

"""Google Cloud Transcoder sample for creating a job based on a supplied job config that includes a static overlay.

Example usage:
    python create_job_with_static_overlay.py --project_id <project-id> --location <location> --input_uri <uri> --overlay_image_uri <uri> --output_uri <uri>
"""

# [START transcoder_create_job_with_static_overlay]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)
from google.protobuf import duration_pb2 as duration


def create_job_with_static_overlay(
    project_id, location, input_uri, overlay_image_uri, output_uri
):
    """Creates a job based on an ad-hoc job configuration that includes a static image overlay.

    Args:
        project_id: The GCP project ID.
        location: The location to start the job in.
        input_uri: Uri of the video in the Cloud Storage bucket.
        overlay_image_uri: Uri of the image for the overlay in the Cloud Storage bucket.
        output_uri: Uri of the video output folder in the Cloud Storage bucket."""

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1.types.Job()
    job.input_uri = input_uri
    job.output_uri = output_uri
    job.config = transcoder_v1.types.JobConfig(
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
        ],
        overlays=[
            transcoder_v1.types.Overlay(
                image=transcoder_v1.types.Overlay.Image(
                    uri=overlay_image_uri,
                    resolution=transcoder_v1.types.Overlay.NormalizedCoordinate(
                        x=1,
                        y=0.5,
                    ),
                    alpha=1,
                ),
                animations=[
                    transcoder_v1.types.Overlay.Animation(
                        animation_static=transcoder_v1.types.Overlay.AnimationStatic(
                            xy=transcoder_v1.types.Overlay.NormalizedCoordinate(
                                x=0,
                                y=0,
                            ),
                            start_time_offset=duration.Duration(
                                seconds=0,
                            ),
                        ),
                    ),
                    transcoder_v1.types.Overlay.Animation(
                        animation_end=transcoder_v1.types.Overlay.AnimationEnd(
                            start_time_offset=duration.Duration(
                                seconds=10,
                            ),
                        ),
                    ),
                ],
            ),
        ],
    )
    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


# [END transcoder_create_job_with_static_overlay]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location to start this job in.",
        default="us-central1",
    )
    parser.add_argument(
        "--input_uri",
        help="Uri of the video in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--overlay_image_uri",
        help="Uri of the overlay image in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        help="Uri of the video output folder in the Cloud Storage bucket. Must end in '/'.",
        required=True,
    )
    args = parser.parse_args()
    create_job_with_static_overlay(
        args.project_id,
        args.location,
        args.input_uri,
        args.overlay_image_uri,
        args.output_uri,
    )

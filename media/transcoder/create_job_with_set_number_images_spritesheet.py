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

"""Google Cloud Transcoder sample for creating a job that generates two spritesheets from the input video. Each spritesheet contains a set number of images.

Example usage:
    python create_job_with_set_number_images_spritesheet.py --project_id <project-id> --location <location> --input_uri <uri> --output_uri <uri>
"""

# [START transcoder_create_job_with_set_number_images_spritesheet]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)


def create_job_with_set_number_images_spritesheet(
    project_id, location, input_uri, output_uri
):
    """Creates a job based on an ad-hoc job configuration that generates two spritesheets.

    Args:
        project_id: The GCP project ID.
        location: The location to start the job in.
        input_uri: Uri of the video in the Cloud Storage bucket.
        output_uri: Uri of the video output folder in the Cloud Storage bucket."""

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1.types.Job()
    job.input_uri = input_uri
    job.output_uri = output_uri
    job.config = transcoder_v1.types.JobConfig(
        # Create an ad-hoc job. For more information, see https://cloud.google.com/transcoder/docs/how-to/jobs#create_jobs_ad_hoc.
        # See all options for the job config at https://cloud.google.com/transcoder/docs/reference/rest/v1beta1/JobConfig.
        elementary_streams=[
            # This section defines the output video stream.
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
            # This section defines the output audio stream.
            transcoder_v1.types.ElementaryStream(
                key="audio-stream0",
                audio_stream=transcoder_v1.types.AudioStream(
                    codec="aac", bitrate_bps=64000
                ),
            ),
        ],
        # This section multiplexes the output audio and video together into a container.
        mux_streams=[
            transcoder_v1.types.MuxStream(
                key="sd",
                container="mp4",
                elementary_streams=["video-stream0", "audio-stream0"],
            ),
        ],
        # Generate two sprite sheets from the input video into the GCS bucket. For more information, see
        # https://cloud.google.com/transcoder/docs/how-to/generate-spritesheet#generate_set_number_of_images.
        sprite_sheets=[
            # Generate a 10x10 sprite sheet with 64x32px images.
            transcoder_v1.types.SpriteSheet(
                file_prefix="small-sprite-sheet",
                sprite_width_pixels=64,
                sprite_height_pixels=32,
                column_count=10,
                row_count=10,
                total_count=100,
            ),
            # Generate a 10x10 sprite sheet with 128x72px images.
            transcoder_v1.types.SpriteSheet(
                file_prefix="large-sprite-sheet",
                sprite_width_pixels=128,
                sprite_height_pixels=72,
                column_count=10,
                row_count=10,
                total_count=100,
            ),
        ],
    )
    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


# [END transcoder_create_job_with_set_number_images_spritesheet]

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
        "--output_uri",
        help="Uri of the video output folder in the Cloud Storage bucket. Must end in '/'.",
        required=True,
    )
    args = parser.parse_args()
    create_job_with_set_number_images_spritesheet(
        args.project_id,
        args.location,
        args.input_uri,
        args.output_uri,
    )

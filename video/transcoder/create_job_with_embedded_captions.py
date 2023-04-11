#!/usr/bin/env python

# Copyright 2022 Google LLC
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

"""Google Cloud Transcoder sample for creating a job that embeds captions in the output video.

Example usage:
    python create_job_with_embedded_captions.py --project_id <project-id> --location <location> \
      --input_video_uri <uri> --input_captions_uri <uri> --output_uri <uri>
"""

# [START transcoder_create_job_with_embedded_captions]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)


def create_job_with_embedded_captions(
    project_id,
    location,
    input_video_uri,
    input_captions_uri,
    output_uri,
):
    """Creates a job based on an ad-hoc job configuration that embeds closed captions in the output video.

    Args:
        project_id (str): The GCP project ID.
        location (str): The location to start the job in.
        input_video_uri (str): Uri of the input video in the Cloud Storage
          bucket.
        input_captions_uri (str): Uri of the input captions file in the Cloud
          Storage bucket.
        output_uri (str): Uri of the video output folder in the Cloud Storage
          bucket."""

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1.types.Job()
    job.output_uri = output_uri
    job.config = transcoder_v1.types.JobConfig(
        inputs=[
            transcoder_v1.types.Input(
                key="input0",
                uri=input_video_uri,
            ),
            transcoder_v1.types.Input(
                key="caption-input0",
                uri=input_captions_uri,
            ),
        ],
        edit_list=[
            transcoder_v1.types.EditAtom(
                key="atom0",
                inputs=["input0", "caption-input0"],
            ),
        ],
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
                    codec="aac",
                    bitrate_bps=64000,
                ),
            ),
            transcoder_v1.types.ElementaryStream(
                key="cea-stream0",
                text_stream=transcoder_v1.types.TextStream(
                    codec="cea608",
                    mapping_=[
                        transcoder_v1.types.TextStream.TextMapping(
                            atom_key="atom0",
                            input_key="caption-input0",
                            input_track=0,
                        ),
                    ],
                    language_code="en-US",
                    display_name="English",
                ),
            ),
        ],
        mux_streams=[
            transcoder_v1.types.MuxStream(
                key="sd-hls",
                container="ts",
                elementary_streams=["video-stream0", "audio-stream0"],
            ),
            transcoder_v1.types.MuxStream(
                key="sd-dash",
                container="fmp4",
                elementary_streams=["video-stream0"],
            ),
            transcoder_v1.types.MuxStream(
                key="audio-dash",
                container="fmp4",
                elementary_streams=["audio-stream0"],
            ),
        ],
        manifests=[
            transcoder_v1.types.Manifest(
                file_name="manifest.m3u8",
                type_="HLS",
                mux_streams=["sd-hls"],
            ),
            transcoder_v1.types.Manifest(
                file_name="manifest.mpd",
                type_="DASH",
                mux_streams=["sd-dash", "audio-dash"],
            ),
        ],
    )
    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


# [END transcoder_create_job_with_embedded_captions]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location to start this job in.",
        default="us-central1",
    )
    parser.add_argument(
        "--input_video_uri",
        help="Uri of the input video in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--input_captions_uri",
        help="Uri of the input captions file in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        help="Uri of the video output folder in the Cloud Storage bucket. "
        + "Must end in '/'.",
        required=True,
    )
    args = parser.parse_args()
    create_job_with_embedded_captions(
        args.project_id,
        args.location,
        args.input_video_uri,
        args.input_captions_uri,
        args.output_uri,
    )

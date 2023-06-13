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

"""Google Cloud Transcoder sample for creating a job that can use subtitles from a standalone file.

Example usage:
    python create_job_with_standalone_captions.py --project_id <project-id> --location <location> \
      --input_video_uri <uri> --input_subtitles1_uri <uri> --input_subtitles2_uri <uri> --output_uri <uri>
"""

# [START transcoder_create_job_with_standalone_captions]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)
from google.protobuf import duration_pb2 as duration


def create_job_with_standalone_captions(
    project_id,
    location,
    input_video_uri,
    input_subtitles1_uri,
    input_subtitles2_uri,
    output_uri,
):
    """Creates a job based on an ad-hoc job configuration that can use subtitles from a standalone file.

    Args:
        project_id (str): The GCP project ID.
        location (str): The location to start the job in.
        input_video_uri (str): Uri of the input video in the Cloud Storage
          bucket.
        input_subtitles1_uri (str): Uri of an input subtitles file in the Cloud
          Storage bucket.
        input_subtitles2_uri (str): Uri of an input subtitles file in the Cloud
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
                key="subtitle-input-en",
                uri=input_subtitles1_uri,
            ),
            transcoder_v1.types.Input(
                key="subtitle-input-es",
                uri=input_subtitles2_uri,
            ),
        ],
        edit_list=[
            transcoder_v1.types.EditAtom(
                key="atom0",
                inputs=["input0", "subtitle-input-en", "subtitle-input-es"],
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
                key="vtt-stream-en",
                text_stream=transcoder_v1.types.TextStream(
                    codec="webvtt",
                    language_code="en-US",
                    display_name="English",
                    mapping_=[
                        transcoder_v1.types.TextStream.TextMapping(
                            atom_key="atom0",
                            input_key="subtitle-input-en",
                        ),
                    ],
                ),
            ),
            transcoder_v1.types.ElementaryStream(
                key="vtt-stream-es",
                text_stream=transcoder_v1.types.TextStream(
                    codec="webvtt",
                    language_code="es-ES",
                    display_name="Spanish",
                    mapping_=[
                        transcoder_v1.types.TextStream.TextMapping(
                            atom_key="atom0",
                            input_key="subtitle-input-es",
                        ),
                    ],
                ),
            ),
        ],
        mux_streams=[
            transcoder_v1.types.MuxStream(
                key="sd-hls-fmp4",
                container="fmp4",
                elementary_streams=["video-stream0"],
            ),
            transcoder_v1.types.MuxStream(
                key="audio-hls-fmp4",
                container="fmp4",
                elementary_streams=["audio-stream0"],
            ),
            transcoder_v1.types.MuxStream(
                key="text-vtt-en",
                container="vtt",
                elementary_streams=["vtt-stream-en"],
                segment_settings=transcoder_v1.types.SegmentSettings(
                    segment_duration=duration.Duration(
                        seconds=6,
                    ),
                    individual_segments=True,
                ),
            ),
            transcoder_v1.types.MuxStream(
                key="text-vtt-es",
                container="vtt",
                elementary_streams=["vtt-stream-es"],
                segment_settings=transcoder_v1.types.SegmentSettings(
                    segment_duration=duration.Duration(
                        seconds=6,
                    ),
                    individual_segments=True,
                ),
            ),
        ],
        manifests=[
            transcoder_v1.types.Manifest(
                file_name="manifest.m3u8",
                type_="HLS",
                mux_streams=[
                    "sd-hls-fmp4",
                    "audio-hls-fmp4",
                    "text-vtt-en",
                    "text-vtt-es",
                ],
            ),
        ],
    )
    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


# [END transcoder_create_job_with_standalone_captions]

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
        "--input_subtitles1_uri",
        help="Uri of an input subtitles file in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--input_subtitles2_uri",
        help="Uri of an input subtitles file in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        help="Uri of the video output folder in the Cloud Storage bucket. "
        + "Must end in '/'.",
        required=True,
    )
    args = parser.parse_args()
    create_job_with_standalone_captions(
        args.project_id,
        args.location,
        args.input_video_uri,
        args.input_subtitles1_uri,
        args.input_subtitles2_uri,
        args.output_uri,
    )

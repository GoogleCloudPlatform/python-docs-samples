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

"""Google Cloud Transcoder sample for creating a job based on concatenating two input videos.

Example usage:
    python create_job_with_concatenated_inputs.py --project_id <project-id> --location <location> \
      --input1_uri <uri> --start_time_input1 <sec> --end_time_input1 <sec> \
      --input2_uri <uri> --start_time_input2 <sec> --end_time_input2 <sec> \
      --output_uri <uri>
"""

# [START transcoder_create_job_with_concatenated_inputs]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)
from google.protobuf import duration_pb2 as duration


def create_job_with_concatenated_inputs(
    project_id,
    location,
    input1_uri,
    start_time_input1,
    end_time_input1,
    input2_uri,
    start_time_input2,
    end_time_input2,
    output_uri,
):
    """Creates a job based on an ad-hoc job configuration that concatenates two input videos.

    Args:
        project_id (str): The GCP project ID.
        location (str): The location to start the job in.
        input1_uri (str): Uri of the first video in the Cloud Storage bucket.
        start_time_input1 (str): Start time, in fractional seconds ending in 's'
          (e.g., '0s'), relative to the first input video timeline.
        end_time_input1 (str): End time, in fractional seconds ending in 's'
          (e.g., '8.1s'), relative to the first input video timeline.
        input2_uri (str): Uri of the second video in the Cloud Storage bucket.
        start_time_input2 (str): Start time, in fractional seconds ending in 's'
          (e.g., '3.5s'), relative to the second input video timeline.
        end_time_input2 (str): End time, in fractional seconds ending in 's'
          (e.g., '15s'), relative to the second input video timeline.
        output_uri (str): Uri of the video output folder in the Cloud Storage
          bucket."""

    s1 = duration.Duration()
    s1.FromJsonString(start_time_input1)
    e1 = duration.Duration()
    e1.FromJsonString(end_time_input1)

    s2 = duration.Duration()
    s2.FromJsonString(start_time_input2)
    e2 = duration.Duration()
    e2.FromJsonString(end_time_input2)

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1.types.Job()
    job.output_uri = output_uri
    job.config = transcoder_v1.types.JobConfig(
        inputs=[
            transcoder_v1.types.Input(key="input1", uri=input1_uri,),
            transcoder_v1.types.Input(key="input2", uri=input2_uri,),
        ],
        edit_list=[
            transcoder_v1.types.EditAtom(
                key="atom1",
                inputs=["input1"],
                start_time_offset=s1,
                end_time_offset=e1,
            ),
            transcoder_v1.types.EditAtom(
                key="atom2",
                inputs=["input2"],
                start_time_offset=s2,
                end_time_offset=e2,
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
    )
    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


# [END transcoder_create_job_with_concatenated_inputs]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location", help="The location to start this job in.", default="us-central1",
    )
    parser.add_argument(
        "--input1_uri",
        help="Uri of the first video in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--start_time_input1",
        help="Start time, in fractional seconds ending in 's' (e.g., '1.1s'), "
        + "relative to the first input video timeline. Use this field to trim "
        + "content from the beginning of the first video.",
        required=True,
    )
    parser.add_argument(
        "--end_time_input1",
        help="End time, in fractional seconds ending in 's' (e.g., '9.5s'), "
        + "relative to the first input video timeline. Use this field to trim "
        + "content from the end of the first video.",
        required=True,
    )
    parser.add_argument(
        "--input2_uri",
        help="Uri of the second video in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--start_time_input2",
        help="Start time, in fractional seconds ending in 's' (e.g., '1.1s'), "
        + "relative to the second input video timeline. Use this field to trim "
        + "content from the beginning of the second video.",
        required=True,
    )
    parser.add_argument(
        "--end_time_input2",
        help="End time, in fractional seconds ending in 's' (e.g., '9.5s'), "
        + "relative to the second input video timeline. Use this field to trim "
        + "content from the end of the second video.",
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        help="Uri of the video output folder in the Cloud Storage bucket. "
        + "Must end in '/'.",
        required=True,
    )
    args = parser.parse_args()
    create_job_with_concatenated_inputs(
        args.project_id,
        args.location,
        args.input1_uri,
        args.start_time_input1,
        args.end_time_input1,
        args.input2_uri,
        args.start_time_input2,
        args.end_time_input2,
        args.output_uri,
    )

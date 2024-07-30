# Copyright 2023 Google LLC
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

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)
from google.protobuf import timestamp_pb2

seconds_per_hour = 3600


def delete_stale_slates(project_id: str, location: str) -> None:
    """Lists all outdated slates in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the slates."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_slates(parent=parent)

    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()

    for slate in response.slates:
        tmp = slate.name.split("-")
        try:
            creation_time_sec = int(tmp.pop())
        except ValueError:
            continue
        if (now.seconds - creation_time_sec) > (3 * seconds_per_hour):
            response = client.delete_slate(name=slate.name)


def delete_stale_cdn_keys(project_id: str, location: str) -> None:
    """Lists all outdated CDN keys in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the CDN keys."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_cdn_keys(parent=parent)

    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()

    for cdn_key in response.cdn_keys:
        tmp = cdn_key.name.split("-")
        try:
            creation_time_sec = int(tmp.pop())
        except ValueError:
            continue
        if (now.seconds - creation_time_sec) > (3 * seconds_per_hour):
            response = client.delete_cdn_key(name=cdn_key.name)


def delete_stale_live_configs(project_id: str, location: str) -> None:
    """Lists all outdated live configs in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the live configs."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_live_configs(parent=parent)

    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()

    for live_config in response.live_configs:
        tmp = live_config.name.split("-")
        try:
            creation_time_sec = int(tmp.pop())
        except ValueError:
            continue
        if (now.seconds - creation_time_sec) > (3 * seconds_per_hour):
            response = client.delete_live_config(name=live_config.name)


def delete_stale_vod_configs(project_id: str, location: str) -> None:
    """Lists all outdated VOD configs in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the VOD configs."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_vod_configs(parent=parent)

    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()

    for vod_config in response.vod_configs:
        tmp = vod_config.name.split("-")
        try:
            creation_time_sec = int(tmp.pop())
        except ValueError:
            continue
        if (now.seconds - creation_time_sec) > (3 * seconds_per_hour):
            response = client.delete_vod_config(name=vod_config.name)

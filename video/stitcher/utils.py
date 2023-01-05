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
        creation_time_sec = int(tmp.pop())
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
        creation_time_sec = int(tmp.pop())
        if (now.seconds - creation_time_sec) > (3 * seconds_per_hour):
            response = client.delete_cdn_key(name=cdn_key.name)

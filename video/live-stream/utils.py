from google.protobuf import timestamp_pb2

seconds_per_hour = 3600


def is_resource_stale(create_time: str) -> bool:
    """Checks the create timestamp to see if the resource is stale (and should be deleted).
    Args:
        create_time: Creation time in Timestamp format."""
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(create_time)
    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()
    if (now.seconds - timestamp.seconds) > (3 * seconds_per_hour):
        return True
    else:
        return False

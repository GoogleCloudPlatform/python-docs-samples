#!/usr/bin/env python

# Copyright 2026 Google LLC
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
"""
command line application and sample code for reconfiguring the recurring
rotation schedule on a Cloud SQL DB credentials secret.
"""

# [START secretmanager_update_regional_secret_with_managed_rotation_schedule]
import argparse
import time

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1
from google.protobuf.duration_pb2 import Duration
from google.protobuf.timestamp_pb2 import Timestamp


def update_regional_secret_with_managed_rotation_schedule(
    project_id: str,
    location_id: str,
    secret_id: str,
    rotation_period_seconds: int,
) -> secretmanager_v1.Secret:
    """
    Reconfigure the recurring rotation schedule on a secret that already
    has Cloud SQL managed rotation enabled (see
    enable_regional_secret_managed_rotation.py). This only applies to
    regional secrets of the CLOUD_SQL_DB_CREDENTIALS type -- calling it on
    any other secret type, or before managed rotation has been enabled,
    fails.

    rotation_period_seconds is the interval between rotations, in whole
    seconds. The service requires it to be at least 3600 (1 hour), and the
    derived next_rotation_time (now + rotation_period_seconds) must be at
    least 300 seconds (5 minutes) in the future -- both are enforced by the
    API, not checked client-side here.
    """

    # Endpoint to call the regional Secret Manager API.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret.
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # next_rotation_time and rotation_period must be set together.
    next_rotation_timestamp = int(time.time()) + rotation_period_seconds

    # Build the updated secret.
    secret = {
        "name": name,
        "rotation": {
            "next_rotation_time": Timestamp(seconds=next_rotation_timestamp),
            "rotation_period": Duration(seconds=rotation_period_seconds),
        },
    }

    # Mask only the two subfields being set here, not the whole "rotation"
    # submessage -- that would also include managed_rotation_status, which
    # is output-only and rejects a whole-submessage replace with "immutable
    # and cannot be updated" (confirmed empirically against a live
    # project).
    update_mask = {"paths": ["rotation.next_rotation_time", "rotation.rotation_period"]}

    # Update the secret.
    response = client.update_secret(
        request={"secret": secret, "update_mask": update_mask}
    )

    print(f"Updated regional secret rotation schedule: {response.name}")

    return response


# [END secretmanager_update_regional_secret_with_managed_rotation_schedule]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument(
        "secret_id",
        help="id of the Cloud SQL DB credentials secret to reconfigure",
    )
    parser.add_argument(
        "rotation_period_seconds",
        type=int,
        help="seconds between rotations; must be at least 3600 (1 hour)",
    )
    args = parser.parse_args()

    update_regional_secret_with_managed_rotation_schedule(
        args.project_id,
        args.location_id,
        args.secret_id,
        args.rotation_period_seconds,
    )

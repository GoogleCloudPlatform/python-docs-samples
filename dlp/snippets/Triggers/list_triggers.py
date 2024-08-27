# Copyright 2023 Google LLC
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
# limitations under the License.

"""Sample app that sets up Data Loss Prevention API automation triggers."""

import argparse


# [START dlp_list_triggers]
import google.cloud.dlp


def list_triggers(project: str) -> None:
    """Lists all Data Loss Prevention API triggers.
    Args:
        project: The Google Cloud project id to use as a parent resource.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.list_job_triggers(request={"parent": parent})

    for trigger in response:
        print(f"Trigger {trigger.name}:")
        print(f"  Created: {trigger.create_time}")
        print(f"  Updated: {trigger.update_time}")
        if trigger.display_name:
            print(f"  Display Name: {trigger.display_name}")
        if trigger.description:
            print(f"  Description: {trigger.description}")
        print(f"  Status: {trigger.status}")
        print(f"  Error count: {len(trigger.errors)}")


# [END dlp_list_triggers]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )

    args = parser.parse_args()

    list_triggers(args.project)

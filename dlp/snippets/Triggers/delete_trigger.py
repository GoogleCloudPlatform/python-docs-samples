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


# [START dlp_delete_trigger]
import google.cloud.dlp


def delete_trigger(project: str, trigger_id: str) -> None:
    """Deletes a Data Loss Prevention API trigger.
    Args:
        project: The id of the Google Cloud project which owns the trigger.
        trigger_id: The id of the trigger to delete.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Combine the trigger id with the parent id.
    trigger_resource = f"{parent}/jobTriggers/{trigger_id}"

    # Call the API.
    dlp.delete_job_trigger(request={"name": trigger_resource})

    print(f"Trigger {trigger_resource} successfully deleted.")


# [END dlp_delete_trigger]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trigger_id", help="The id of the trigger to delete.")
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )

    args = parser.parse_args()

    delete_trigger(args.project, args.trigger_id)

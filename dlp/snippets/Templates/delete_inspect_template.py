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

"""Sample app that sets up Data Loss Prevention API inspect templates."""

import argparse


# [START dlp_delete_inspect_template]
import google.cloud.dlp


def delete_inspect_template(project: str, template_id: str) -> None:
    """Deletes a Data Loss Prevention API template.
    Args:
        project: The id of the Google Cloud project which owns the template.
        template_id: The id of the template to delete.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Combine the template id with the parent id.
    template_resource = f"{parent}/inspectTemplates/{template_id}"

    # Call the API.
    dlp.delete_inspect_template(request={"name": template_resource})

    print(f"Template {template_resource} successfully deleted.")


# [END dlp_delete_inspect_template]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("template_id", help="The id of the template to delete.")
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )

    args = parser.parse_args()
    delete_inspect_template(args.project, args.template_id)

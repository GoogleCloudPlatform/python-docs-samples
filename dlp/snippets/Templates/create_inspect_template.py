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


# [START dlp_create_inspect_template]
from typing import List
from typing import Optional

import google.cloud.dlp


def create_inspect_template(
    project: str,
    info_types: List[str],
    template_id: Optional[str] = None,
    display_name: Optional[str] = None,
    min_likelihood: Optional[int] = None,
    max_findings: Optional[int] = None,
    include_quote: Optional[bool] = None,
) -> None:
    """Creates a Data Loss Prevention API inspect template.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        template_id: The id of the template. If omitted, an id will be randomly
            generated.
        display_name: The optional display name of the template.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": min_likelihood,
        "include_quote": include_quote,
        "limits": {"max_findings_per_request": max_findings},
    }

    inspect_template = {
        "inspect_config": inspect_config,
        "display_name": display_name,
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.create_inspect_template(
        request={
            "parent": parent,
            "inspect_template": inspect_template,
            "template_id": template_id,
        }
    )

    print(f"Successfully created template {response.name}")


# [END dlp_create_inspect_template]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--template_id",
        help="The id of the template. If omitted, an id will be randomly " "generated",
    )
    parser.add_argument(
        "--display_name", help="The optional display name of the template."
    )
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser.add_argument(
        "--min_likelihood",
        choices=[
            "LIKELIHOOD_UNSPECIFIED",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ],
        help="A string representing the minimum likelihood threshold that "
        "constitutes a match.",
    )
    parser.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser.add_argument(
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )

    args = parser.parse_args()

    create_inspect_template(
        args.project,
        args.info_types,
        template_id=args.template_id,
        display_name=args.display_name,
        min_likelihood=args.min_likelihood,
        max_findings=args.max_findings,
        include_quote=args.include_quote,
    )

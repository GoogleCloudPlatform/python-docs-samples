# Copyright 2024 Google LLC
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

"""Sample app that uses the Data Loss Prevention API to inspect a string, a
local file or a file on Google Cloud Storage."""


import argparse

# [START dlp_inspect_string_rep]
from typing import List

import google.cloud.dlp


def inspect_string(
    project: str,
    rep_location: str,
    content_string: str,
    info_types: List[str],
    include_quote: bool = True,
) -> None:
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        rep_location: The location of regional endpoint to use.
        content_string: The string to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Assemble the regional endpoint url using provided rep location
    rep_endpoint = f"dlp.{rep_location}.rep.googleapis.com"
    client_options = {"api_endpoint": rep_endpoint}

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient(client_options=client_options)

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "include_quote": include_quote,
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/{rep_location}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            try:
                if finding.quote:
                    print(f"Quote: {finding.quote}")
            except AttributeError:
                pass
            print(f"Info type: {finding.info_type.name}")
            print(f"Likelihood: {finding.likelihood}")
    else:
        print("No findings.")


# [END dlp_inspect_string_rep]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("item", help="The string to inspect.")
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--rep_location",
        help="The regional endpoint location to use.",
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
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )
    args = parser.parse_args()

    inspect_string(
        args.project,
        args.rep_location,
        args.item,
        args.info_types,
        include_quote=args.include_quote,
    )

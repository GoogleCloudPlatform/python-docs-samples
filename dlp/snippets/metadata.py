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

"""Sample app that queries the Data Loss Prevention API for supported
categories and info types."""


import argparse


# [START dlp_list_info_types]
def list_info_types(language_code=None, result_filter=None):
    """List types of sensitive information within a category.
    Args:
        language_code: The BCP-47 language code to use, e.g. 'en-US'.
        filter: An optional filter to only return info types supported by
                certain parts of the API. Defaults to "supported_by=INSPECT".
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Make the API call.
    response = dlp.list_info_types(
        request={"parent": language_code, "filter": result_filter}
    )

    # Print the results to the console.
    print("Info types:")
    for info_type in response.info_types:
        print(
            "{name}: {display_name}".format(
                name=info_type.name, display_name=info_type.display_name
            )
        )


# [END dlp_list_info_types]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--language_code",
        help="The BCP-47 language code to use, e.g. 'en-US'.",
    )
    parser.add_argument(
        "--filter",
        help="An optional filter to only return info types supported by "
        'certain parts of the API. Defaults to "supported_by=INSPECT".',
    )

    args = parser.parse_args()

    list_info_types(language_code=args.language_code, result_filter=args.filter)

# Copyright 2017 Google Inc.
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

from __future__ import print_function

import argparse
import os


# [START dlp_create_inspect_template]
def create_inspect_template(
    project,
    info_types,
    template_id=None,
    display_name=None,
    min_likelihood=None,
    max_findings=None,
    include_quote=None,
):
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

    # Import the client library
    import google.cloud.dlp

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

    print("Successfully created template {}".format(response.name))


# [END dlp_create_inspect_template]


# [START dlp_list_templates]
def list_inspect_templates(project):
    """Lists all Data Loss Prevention API inspect templates.
    Args:
        project: The Google Cloud project id to use as a parent resource.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.list_inspect_templates(request={"parent": parent})

    for template in response:
        print("Template {}:".format(template.name))
        if template.display_name:
            print("  Display Name: {}".format(template.display_name))
        print("  Created: {}".format(template.create_time))
        print("  Updated: {}".format(template.update_time))

        config = template.inspect_config
        print(
            "  InfoTypes: {}".format(", ".join([it.name for it in config.info_types]))
        )
        print("  Minimum likelihood: {}".format(config.min_likelihood))
        print("  Include quotes: {}".format(config.include_quote))
        print(
            "  Max findings per request: {}".format(
                config.limits.max_findings_per_request
            )
        )


# [END dlp_list_templates]


# [START dlp_delete_inspect_template]
def delete_inspect_template(project, template_id):
    """Deletes a Data Loss Prevention API template.
    Args:
        project: The id of the Google Cloud project which owns the template.
        template_id: The id of the template to delete.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Combine the template id with the parent id.
    template_resource = "{}/inspectTemplates/{}".format(parent, template_id)

    # Call the API.
    dlp.delete_inspect_template(request={"name": template_resource})

    print("Template {} successfully deleted.".format(template_resource))


# [END dlp_delete_inspect_template]


if __name__ == "__main__":
    default_project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="action", help="Select which action to perform."
    )
    subparsers.required = True

    parser_create = subparsers.add_parser("create", help="Create a template.")
    parser_create.add_argument(
        "--template_id",
        help="The id of the template. If omitted, an id will be randomly " "generated",
    )
    parser_create.add_argument(
        "--display_name", help="The optional display name of the template."
    )
    parser_create.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_create.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_create.add_argument(
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
    parser_create.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_create.add_argument(
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )

    parser_list = subparsers.add_parser("list", help="List all templates.")
    parser_list.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )

    parser_delete = subparsers.add_parser("delete", help="Delete a template.")
    parser_delete.add_argument("template_id", help="The id of the template to delete.")
    parser_delete.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )

    args = parser.parse_args()

    if args.action == "create":
        create_inspect_template(
            args.project,
            args.info_types,
            template_id=args.template_id,
            display_name=args.display_name,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            include_quote=args.include_quote,
        )
    elif args.action == "list":
        list_inspect_templates(args.project)
    elif args.action == "delete":
        delete_inspect_template(args.project, args.template_id)

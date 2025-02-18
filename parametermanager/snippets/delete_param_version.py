#!/usr/bin/env python

# Copyright 2025 Google LLC
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
command line application and sample code for deleting a parameter version.
"""

import argparse


# [START parametermanager_delete_param_version]
def delete_param_version(project_id: str, parameter_id: str, version_id: str) -> None:
    """
    Deletes a specific version of an existing parameter in the global location
    of the specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        parameter_id (str): The ID of the parameter for
        which the version is to be deleted.
        version_id (str): The ID of the version to be deleted.

    Returns:
        None

    Example:
        delete_param_version(
            "my-project",
            "my-global-parameter",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parameter version.
    name = client.parameter_version_path(
            project_id, "global", parameter_id, version_id
    )

    # Define the request to delete the parameter version.
    request = parametermanager_v1.DeleteParameterVersionRequest(name=name)

    # Delete the parameter version.
    client.delete_parameter_version(request=request)

    # Print a confirmation message.
    print(f"Deleted Parameter Version: {name}")
    # [END parametermanager_delete_param_version]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("param_id", help="id of the parameter to create")
    parser.add_argument(
        "version_id", help="id of the version of the parameter to create"
    )
    args = parser.parse_args()

    delete_param_version(args.project_id, args.param_id, args.version_id)

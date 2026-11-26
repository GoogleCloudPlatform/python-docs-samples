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
command line application and sample code for
listing the template versions.
"""


# [START parametermanager_list_param_template_versions]
def list_param_template_versions(project_id: str, template_id: str) -> None:
    """
    Lists all versions of an existing template in the global location of the
    specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project.
        template_id (str): The ID of the template for which versions are to be
        listed.

    Returns:
        None

    Example:
        list_param_template_versions(
            "my-project",
            "my-template"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the template.
    parent = client.template_path(project_id, "global", template_id)

    # List the versions of the template.
    for version in client.list_template_versions(parent=parent):
        print(f"Found template version: {version.name}")
    # [END parametermanager_list_param_template_versions]

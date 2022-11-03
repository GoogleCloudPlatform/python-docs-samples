#!/usr/bin/env python

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os

from google.api_core.client_options import ClientOptions


# [START datalabeling_create_dataset_beta]
def create_dataset(project_id):
    """Creates a dataset for the given Google Cloud project."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_create_dataset_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_create_dataset_beta]

    formatted_project_name = f"projects/{project_id}"

    dataset = datalabeling.Dataset(
        display_name="YOUR_DATASET_SET_DISPLAY_NAME", description="YOUR_DESCRIPTION"
    )

    response = client.create_dataset(
        request={"parent": formatted_project_name, "dataset": dataset}
    )

    # The format of resource name:
    # project_id/{project_id}/datasets/{dataset_id}
    print("The dataset resource name: {}".format(response.name))
    print("Display name: {}".format(response.display_name))
    print("Description: {}".format(response.description))
    print("Create time:")
    print("\tseconds: {}".format(response.create_time.timestamp_pb().seconds))
    print("\tnanos: {}\n".format(response.create_time.timestamp_pb().nanos))

    return response


# [END datalabeling_create_dataset_beta]


# [START datalabeling_list_datasets_beta]
def list_datasets(project_id):
    """Lists datasets for the given Google Cloud project."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_list_datasets_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_list_datasets_beta]

    formatted_project_name = f"projects/{project_id}"

    response = client.list_datasets(request={"parent": formatted_project_name})
    for element in response:
        # The format of resource name:
        # project_id/{project_id}/datasets/{dataset_id}
        print("The dataset resource name: {}\n".format(element.name))
        print("Display name: {}".format(element.display_name))
        print("Description: {}".format(element.description))
        print("Create time:")
        print("\tseconds: {}".format(element.create_time.timestamp_pb().seconds))
        print("\tnanos: {}".format(element.create_time.timestamp_pb().nanos))


# [END datalabeling_list_datasets_beta]


# [START datalabeling_get_dataset_beta]
def get_dataset(dataset_resource_name):
    """Gets a dataset for the given Google Cloud project."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_get_dataset_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_get_dataset_beta]

    response = client.get_dataset(request={"name": dataset_resource_name})

    print("The dataset resource name: {}\n".format(response.name))
    print("Display name: {}".format(response.display_name))
    print("Description: {}".format(response.description))
    print("Create time:")
    print("\tseconds: {}".format(response.create_time.timestamp_pb().seconds))
    print("\tnanos: {}".format(response.create_time.timestamp_pb().nanos))


# [END datalabeling_get_dataset_beta]


# [START datalabeling_delete_dataset_beta]
def delete_dataset(dataset_resource_name):
    """Deletes a dataset for the given Google Cloud project."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_delete_dataset_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_delete_dataset_beta]

    response = client.delete_dataset(request={"name": dataset_resource_name})

    print("Dataset deleted. {}\n".format(response))


# [END datalabeling_delete_dataset_beta]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a new dataset.")
    create_parser.add_argument(
        "--project-id", help="Project ID. Required.", required=True
    )

    list_parser = subparsers.add_parser("list", help="List all datasets.")
    list_parser.add_argument(
        "--project-id", help="Project ID. Required.", required=True
    )

    get_parser = subparsers.add_parser(
        "get", help="Get a dataset by the dataset resource name."
    )
    get_parser.add_argument(
        "--dataset-resource-name",
        help="The dataset resource name. Used in the get or delete operation.",
        required=True,
    )

    delete_parser = subparsers.add_parser(
        "delete", help="Delete a dataset by the dataset resource name."
    )
    delete_parser.add_argument(
        "--dataset-resource-name",
        help="The dataset resource name. Used in the get or delete operation.",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "create":
        create_dataset(args.project_id)
    elif args.command == "list":
        list_datasets(args.project_id)
    elif args.command == "get":
        get_dataset(args.dataset_resource_name)
    elif args.command == "delete":
        delete_dataset(args.dataset_resource_name)

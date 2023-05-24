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


# [START datalabeling_export_data_beta]
def export_data(dataset_resource_name, annotated_dataset_resource_name, export_gcs_uri):
    """Exports a dataset from the given Google Cloud project."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_export_data_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_export_data_beta]

    gcs_destination = datalabeling.GcsDestination(
        output_uri=export_gcs_uri, mime_type="text/csv"
    )

    output_config = datalabeling.OutputConfig(gcs_destination=gcs_destination)

    response = client.export_data(
        request={
            "name": dataset_resource_name,
            "annotated_dataset": annotated_dataset_resource_name,
            "output_config": output_config,
        }
    )

    print(f"Dataset ID: {response.result().dataset}\n")
    print("Output config:")
    print("\tGcs destination:")
    print(
        "\t\tOutput URI: {}\n".format(
            response.result().output_config.gcs_destination.output_uri
        )
    )


# [END datalabeling_export_data_beta]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--dataset-resource-name",
        help="Dataset resource name. Required.",
        required=True,
    )

    parser.add_argument(
        "--annotated-dataset-resource-name",
        help="Annotated Dataset resource name. Required.",
        required=True,
    )

    parser.add_argument(
        "--export-gcs-uri", help="The export GCS URI. Required.", required=True
    )

    args = parser.parse_args()

    export_data(
        args.dataset_resource_name,
        args.annotated_dataset_resource_name,
        args.export_gcs_uri,
    )

#!/usr/bin/env python

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on dataset
with the Google AutoML Translation API.

For more information, see the documentation at
https://cloud.google.com/translate/automl/docs
"""

import argparse
import os


def import_data(project_id, compute_region, dataset_id, path):
    """Import sentence pairs to the dataset."""
    # [START automl_translate_import_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # path = 'gs://path/to/file.csv'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(project_id, compute_region, dataset_id)

    # Get the multiple Google Cloud Storage URIs
    input_uris = path.split(",")
    input_config = {"gcs_source": {"input_uris": input_uris}}

    # Import data from the input URI
    response = client.import_data(name=dataset_full_id, input_config=input_config)

    print("Processing import...")
    # synchronous check of operation status
    print("Data imported. {}".format(response.result()))

    # [END automl_translate_import_data]


def delete_dataset(project_id, compute_region, dataset_id):
    """Delete a dataset."""
    # [START automl_translate_delete_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(project_id, compute_region, dataset_id)

    # Delete a dataset.
    response = client.delete_dataset(name=dataset_full_id)

    # synchronous check of operation status
    print("Dataset deleted. {}".format(response.result()))

    # [END automl_translate_delete_dataset]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    import_data_parser = subparsers.add_parser("import_data", help=import_data.__doc__)
    import_data_parser.add_argument("dataset_id")
    import_data_parser.add_argument("path")

    delete_dataset_parser = subparsers.add_parser(
        "delete_dataset", help=delete_dataset.__doc__
    )
    delete_dataset_parser.add_argument("dataset_id")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "import_data":
        import_data(project_id, compute_region, args.dataset_id, args.path)
    if args.command == "delete_dataset":
        delete_dataset(project_id, compute_region, args.dataset_id)

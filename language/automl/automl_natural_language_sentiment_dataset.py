#!/usr/bin/env python

# Copyright 2019 Google LLC
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

"""This application demonstrates how to perform basic operations on Dataset
with the Google AutoML Natural Language API.

For more information, see the tutorial page at
https://cloud.google.com/natural-language/automl/docs/
"""

import argparse
import os
from datetime import datetime

def create_dataset(project_id, compute_region, dataset_name, sentiment_max):
    """Create a dataset for sentiment."""
    # [START automl_natural_language_create_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # dataset_name = '[DATASET_NAME]'
    # sentiment_max = Integer score for sentiment with max of 10

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Specify the sentiment score for the dataset.
    dataset_metadata = {"sentiment_max": sentiment_max}

    # Set dataset name and metadata.
    my_dataset = {
        "display_name": dataset_name,
        "text_sentiment_dataset_metadata": dataset_metadata,
    }

    # Create a dataset with the dataset metadata in the region.
    dataset = client.create_dataset(project_location, my_dataset)

    # Display the dataset information.
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Text sentiment dataset metadata:")
    print("\t{}".format(dataset.text_sentiment_dataset_metadata))
    print("Dataset example count: {}".format(dataset.example_count))
    print("Model create time: {}".format(datetime.fromtimestamp(dataset.create_time.seconds).strftime("%Y-%m-%dT%H:%M:%SZ")))

    # [END automl_natural_language_create_dataset]


def list_datasets(project_id, compute_region, filter_):
    """List all datasets."""
    # [START automl_natural_language_list_datasets]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # filter_ = 'text_sentiment_dataset_metadata:*'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # List all the datasets available in the region by applying filter.
    response = client.list_datasets(project_location, filter_)

    print("List of datasets:")
    for dataset in response:
        # Display the dataset information.
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        print("Text sentiment dataset metadata:")
        print("\t{}".format(dataset.text_sentiment_dataset_metadata))
        print("Dataset example count: {}".format(dataset.example_count))
        print("Model create time: {}".format(datetime.fromtimestamp(dataset.create_time.seconds).strftime("%Y-%m-%dT%H:%M:%SZ")))

    # [END automl_natural_language_list_datasets]


def get_dataset(project_id, compute_region, dataset_id):
    """Get the dataset."""
    # [START automl_natural_language_get_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # dataset_id = '[DATASET_ID]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Get complete detail of the dataset.
    dataset = client.get_dataset(dataset_full_id)

    # Display the dataset information.
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Text sentiment dataset metadata:")
    print("\t{}".format(dataset.text_sentiment_dataset_metadata))
    print("Dataset example count: {}".format(dataset.example_count))
    print("Model create time: {}".format(datetime.fromtimestamp(dataset.create_time.seconds).strftime("%Y-%m-%dT%H:%M:%SZ")))

    # [END automl_natural_language_get_dataset]


def import_data(project_id, compute_region, dataset_id, path):
    """Import labelled items."""
    # [START automl_natural_language_import_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # dataset_id = '[DATASET_ID]'
    # path = 'gs://path/to/file.csv'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Get the multiple Google Cloud Storage URIs.
    input_uris = path.split(",")
    input_config = {"gcs_source": {"input_uris": input_uris}}

    # Import the dataset from the input URI.
    response = client.import_data(dataset_full_id, input_config)

    print("Processing import...")
    # synchronous check of operation status.
    print("Data imported. {}".format(response.result()))

    # [END automl_natural_language_import_data]


def export_data(project_id, compute_region, dataset_id, output_uri):
    """Export a dataset to a Google Cloud Storage bucket."""
    # [START automl_natural_language_export_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # dataset_id = '[DATASET_ID]'
    # output_uri: 'gs://location/to/export/data'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Set the output URI
    output_config = {"gcs_destination": {"output_uri_prefix": output_uri}}

    # Export the data to the output URI.
    response = client.export_data(dataset_full_id, output_config)

    print("Processing export...")
    # synchronous check of operation status.
    print("Data exported. {}".format(response.result()))

    # [END automl_natural_language_export_data]


def delete_dataset(project_id, compute_region, dataset_id):
    """Delete a dataset."""
    # [START automl_natural_language_delete_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # dataset_id = '[DATASET_ID]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Delete a dataset.
    response = client.delete_dataset(dataset_full_id)

    # synchronous check of operation status.
    print("Dataset deleted. {}".format(response.result()))

    # [END automl_natural_language_delete_dataset]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    create_dataset_parser = subparsers.add_parser(
        "create_dataset", help=create_dataset.__doc__
    )
    create_dataset_parser.add_argument("dataset_name")
    create_dataset_parser.add_argument("sentiment_max")

    list_datasets_parser = subparsers.add_parser(
        "list_datasets", help=list_datasets.__doc__
    )
    list_datasets_parser.add_argument(
        "filter_", nargs="?", default="text_sentiment_dataset_metadata:*"
    )

    get_dataset_parser = subparsers.add_parser(
        "get_dataset", help=get_dataset.__doc__
    )
    get_dataset_parser.add_argument("dataset_id")

    import_data_parser = subparsers.add_parser(
        "import_data", help=import_data.__doc__
    )
    import_data_parser.add_argument("dataset_id")
    import_data_parser.add_argument(
      "path", nargs="?", default="gs://cloud-ml-data/NL-entity/dataset.csv"
    )

    export_data_parser = subparsers.add_parser(
        "export_data", help=export_data.__doc__
    )
    export_data_parser.add_argument("dataset_id")
    export_data_parser.add_argument("output_uri")

    delete_dataset_parser = subparsers.add_parser(
        "delete_dataset", help=delete_dataset.__doc__
    )
    delete_dataset_parser.add_argument("dataset_id")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "create_dataset":
        sentiment_max = int(args.sentiment_max)
        create_dataset(
            project_id, compute_region, args.dataset_name, sentiment_max
        )
    if args.command == "list_datasets":
        list_datasets(project_id, compute_region, args.filter_)
    if args.command == "get_dataset":
        get_dataset(project_id, compute_region, args.dataset_id)
    if args.command == "import_data":
        import_data(project_id, compute_region, args.dataset_id, args.path)
    if args.command == "export_data":
        export_data(
            project_id, compute_region, args.dataset_id, args.output_uri
        )
    if args.command == "delete_dataset":
        delete_dataset(project_id, compute_region, args.dataset_id)

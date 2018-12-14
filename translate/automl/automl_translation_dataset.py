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


def create_dataset(project_id, compute_region, dataset_name, source, target):
    """Create a dataset."""
    # [START automl_translate_create_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_name = 'DATASET_NAME_HERE'
    # source = 'LANGUAGE_CODE_OF_SOURCE_LANGUAGE'
    # target = 'LANGUAGE_CODE_OF_TARGET_LANGUAGE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Specify the source and target language.
    dataset_metadata = {
        "source_language_code": source,
        "target_language_code": target,
    }
    # Set dataset name and dataset metadata
    my_dataset = {
        "display_name": dataset_name,
        "translation_dataset_metadata": dataset_metadata,
    }

    # Create a dataset with the dataset metadata in the region.
    dataset = client.create_dataset(project_location, my_dataset)

    # Display the dataset information
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Translation dataset Metadata:")
    print(
        "\tsource_language_code: {}".format(
            dataset.translation_dataset_metadata.source_language_code
        )
    )
    print(
        "\ttarget_language_code: {}".format(
            dataset.translation_dataset_metadata.target_language_code
        )
    )
    print("Dataset create time:")
    print("\tseconds: {}".format(dataset.create_time.seconds))
    print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_translate_create_dataset]


def list_datasets(project_id, compute_region, filter_):
    """List Datasets."""
    # [START automl_translate_list_datasets]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # List all the datasets available in the region by applying filter.
    response = client.list_datasets(project_location, filter_)

    print("List of datasets:")
    for dataset in response:
        # Display the dataset information
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        print("Translation dataset metadata:")
        print(
            "\tsource_language_code: {}".format(
                dataset.translation_dataset_metadata.source_language_code
            )
        )
        print(
            "\ttarget_language_code: {}".format(
                dataset.translation_dataset_metadata.target_language_code
            )
        )
        print("Dataset create time:")
        print("\tseconds: {}".format(dataset.create_time.seconds))
        print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_translate_list_datasets]


def get_dataset(project_id, compute_region, dataset_id):
    """Get the dataset."""
    # [START automl_translate_get_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Get complete detail of the dataset.
    dataset = client.get_dataset(dataset_full_id)

    # Display the dataset information
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Translation dataset metadata:")
    print(
        "\tsource_language_code: {}".format(
            dataset.translation_dataset_metadata.source_language_code
        )
    )
    print(
        "\ttarget_language_code: {}".format(
            dataset.translation_dataset_metadata.target_language_code
        )
    )
    print("Dataset create time:")
    print("\tseconds: {}".format(dataset.create_time.seconds))
    print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_translate_get_dataset]


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
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Get the multiple Google Cloud Storage URIs
    input_uris = path.split(",")
    input_config = {"gcs_source": {"input_uris": input_uris}}

    # Import data from the input URI
    response = client.import_data(dataset_full_id, input_config)

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
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Delete a dataset.
    response = client.delete_dataset(dataset_full_id)

    # synchronous check of operation status
    print("Dataset deleted. {}".format(response.result()))

    # [END automl_translate_delete_dataset]


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
    create_dataset_parser.add_argument("source")
    create_dataset_parser.add_argument("target")

    list_datasets_parser = subparsers.add_parser(
        "list_datasets", help=list_datasets.__doc__
    )
    list_datasets_parser.add_argument("filter", nargs="?", default="")

    import_data_parser = subparsers.add_parser(
        "import_data", help=import_data.__doc__
    )
    import_data_parser.add_argument("dataset_id")
    import_data_parser.add_argument("path")

    delete_dataset_parser = subparsers.add_parser(
        "delete_dataset", help=delete_dataset.__doc__
    )
    delete_dataset_parser.add_argument("dataset_id")

    get_dataset_parser = subparsers.add_parser(
        "get_dataset", help=get_dataset.__doc__
    )
    get_dataset_parser.add_argument("dataset_id")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "create_dataset":
        create_dataset(
            project_id,
            compute_region,
            args.dataset_name,
            args.source,
            args.target,
        )
    if args.command == "list_datasets":
        list_datasets(project_id, compute_region, args.filter)
    if args.command == "get_dataset":
        get_dataset(project_id, compute_region, args.dataset_id)
    if args.command == "import_data":
        import_data(project_id, compute_region, args.dataset_id, args.path)
    if args.command == "delete_dataset":
        delete_dataset(project_id, compute_region, args.dataset_id)

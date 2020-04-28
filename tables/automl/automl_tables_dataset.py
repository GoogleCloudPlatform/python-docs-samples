#!/usr/bin/env python

# Copyright 2019 Google LLC
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

"""This application demonstrates how to perform basic operations on dataset
with the Google AutoML Tables API.

For more information, the documentation at
https://cloud.google.com/automl-tables/docs.
"""

import argparse
import os


def create_dataset(project_id, compute_region, dataset_display_name):
    """Create a dataset."""
    # [START automl_tables_create_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_display_name = 'DATASET_DISPLAY_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Create a dataset with the given display name
    dataset = client.create_dataset(dataset_display_name)

    # Display the dataset information.
    print("Dataset name: {}".format(dataset.name))
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print("Dataset display name: {}".format(dataset.display_name))
    print("Dataset metadata:")
    print("\t{}".format(dataset.tables_dataset_metadata))
    print("Dataset example count: {}".format(dataset.example_count))
    print("Dataset create time:")
    print("\tseconds: {}".format(dataset.create_time.seconds))
    print("\tnanos: {}".format(dataset.create_time.nanos))

    # [END automl_tables_create_dataset]

    return dataset


def list_datasets(project_id, compute_region, filter_=None):
    """List all datasets."""
    result = []
    # [START automl_tables_list_datasets]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # List all the datasets available in the region by applying filter.
    response = client.list_datasets(filter_=filter_)

    print("List of datasets:")
    for dataset in response:
        # Display the dataset information.
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        metadata = dataset.tables_dataset_metadata
        print(
            "Dataset primary table spec id: {}".format(
                metadata.primary_table_spec_id
            )
        )
        print(
            "Dataset target column spec id: {}".format(
                metadata.target_column_spec_id
            )
        )
        print(
            "Dataset target column spec id: {}".format(
                metadata.target_column_spec_id
            )
        )
        print(
            "Dataset weight column spec id: {}".format(
                metadata.weight_column_spec_id
            )
        )
        print(
            "Dataset ml use column spec id: {}".format(
                metadata.ml_use_column_spec_id
            )
        )
        print("Dataset example count: {}".format(dataset.example_count))
        print("Dataset create time:")
        print("\tseconds: {}".format(dataset.create_time.seconds))
        print("\tnanos: {}".format(dataset.create_time.nanos))
        print("\n")

        # [END automl_tables_list_datasets]
        result.append(dataset)

    return result


def import_data(project_id, compute_region, dataset_display_name, path):
    """Import structured data."""
    # [START automl_tables_import_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_display_name = 'DATASET_DISPLAY_NAME'
    # path = 'gs://path/to/file.csv' or 'bq://project_id.dataset.table_id'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    response = None
    if path.startswith("bq"):
        response = client.import_data(
            dataset_display_name=dataset_display_name, bigquery_input_uri=path
        )
    else:
        # Get the multiple Google Cloud Storage URIs.
        input_uris = path.split(",")
        response = client.import_data(
            dataset_display_name=dataset_display_name,
            gcs_input_uris=input_uris,
        )

    print("Processing import...")
    # synchronous check of operation status.
    print("Data imported. {}".format(response.result()))

    # [END automl_tables_import_data]


def delete_dataset(project_id, compute_region, dataset_display_name):
    """Delete a dataset"""
    # [START automl_tables_delete_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_display_name = 'DATASET_DISPLAY_NAME_HERE

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Delete a dataset.
    response = client.delete_dataset(dataset_display_name=dataset_display_name)

    # synchronous check of operation status.
    print("Dataset deleted. {}".format(response.result()))
    # [END automl_tables_delete_dataset]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    create_dataset_parser = subparsers.add_parser(
        "create_dataset", help=create_dataset.__doc__
    )
    create_dataset_parser.add_argument("--dataset_name")

    list_datasets_parser = subparsers.add_parser(
        "list_datasets", help=list_datasets.__doc__
    )
    list_datasets_parser.add_argument("--filter_")

    list_table_specs_parser = subparsers.add_parser(
        "list_table_specs", help=list_table_specs.__doc__
    )
    list_table_specs_parser.add_argument("--dataset_display_name")
    list_table_specs_parser.add_argument("--filter_")

    list_column_specs_parser = subparsers.add_parser(
        "list_column_specs", help=list_column_specs.__doc__
    )
    list_column_specs_parser.add_argument("--dataset_display_name")
    list_column_specs_parser.add_argument("--filter_")

    get_dataset_parser = subparsers.add_parser(
        "get_dataset", help=get_dataset.__doc__
    )
    get_dataset_parser.add_argument("--dataset_display_name")

    get_table_spec_parser = subparsers.add_parser(
        "get_table_spec", help=get_table_spec.__doc__
    )
    get_table_spec_parser.add_argument("--dataset_id")
    get_table_spec_parser.add_argument("--table_spec_id")

    get_column_spec_parser = subparsers.add_parser(
        "get_column_spec", help=get_column_spec.__doc__
    )
    get_column_spec_parser.add_argument("--dataset_id")
    get_column_spec_parser.add_argument("--table_spec_id")
    get_column_spec_parser.add_argument("--column_spec_id")

    import_data_parser = subparsers.add_parser(
        "import_data", help=import_data.__doc__
    )
    import_data_parser.add_argument("--dataset_display_name")
    import_data_parser.add_argument("--path")

    export_data_parser = subparsers.add_parser(
        "export_data", help=export_data.__doc__
    )
    export_data_parser.add_argument("--dataset_display_name")
    export_data_parser.add_argument("--gcs_uri")

    update_dataset_parser = subparsers.add_parser(
        "update_dataset", help=update_dataset.__doc__
    )
    update_dataset_parser.add_argument("--dataset_display_name")
    update_dataset_parser.add_argument("--target_column_spec_name")
    update_dataset_parser.add_argument("--weight_column_spec_name")
    update_dataset_parser.add_argument("--ml_use_column_spec_name")

    update_table_spec_parser = subparsers.add_parser(
        "update_table_spec", help=update_table_spec.__doc__
    )
    update_table_spec_parser.add_argument("--dataset_display_name")
    update_table_spec_parser.add_argument("--time_column_spec_display_name")

    update_column_spec_parser = subparsers.add_parser(
        "update_column_spec", help=update_column_spec.__doc__
    )
    update_column_spec_parser.add_argument("--dataset_display_name")
    update_column_spec_parser.add_argument("--column_spec_display_name")
    update_column_spec_parser.add_argument("--type_code")
    update_column_spec_parser.add_argument("--nullable", type=bool)

    delete_dataset_parser = subparsers.add_parser(
        "delete_dataset", help=delete_dataset.__doc__
    )
    delete_dataset_parser.add_argument("--dataset_display_name")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()
    if args.command == "create_dataset":
        create_dataset(project_id, compute_region, args.dataset_name)
    if args.command == "list_datasets":
        list_datasets(project_id, compute_region, args.filter_)
    if args.command == "list_table_specs":
        list_table_specs(
            project_id, compute_region, args.dataset_display_name, args.filter_
        )
    if args.command == "list_column_specs":
        list_column_specs(
            project_id, compute_region, args.dataset_display_name, args.filter_
        )
    if args.command == "get_dataset":
        get_dataset(project_id, compute_region, args.dataset_display_name)
    if args.command == "get_table_spec":
        get_table_spec(
            project_id,
            compute_region,
            args.dataset_display_name,
            args.table_spec_id,
        )
    if args.command == "get_column_spec":
        get_column_spec(
            project_id,
            compute_region,
            args.dataset_display_name,
            args.table_spec_id,
            args.column_spec_id,
        )
    if args.command == "import_data":
        import_data(
            project_id, compute_region, args.dataset_display_name, args.path
        )
    if args.command == "export_data":
        export_data(
            project_id, compute_region, args.dataset_display_name, args.gcs_uri
        )
    if args.command == "update_dataset":
        update_dataset(
            project_id,
            compute_region,
            args.dataset_display_name,
            args.target_column_spec_name,
            args.weight_column_spec_name,
            args.ml_use_column_spec_name,
        )
    if args.command == "update_table_spec":
        update_table_spec(
            project_id,
            compute_region,
            args.dataset_display_name,
            args.time_column_spec_display_name,
        )
    if args.command == "update_column_spec":
        update_column_spec(
            project_id,
            compute_region,
            args.dataset_display_name,
            args.column_spec_display_name,
            args.type_code,
            args.nullable,
        )
    if args.command == "delete_dataset":
        delete_dataset(project_id, compute_region, args.dataset_display_name)

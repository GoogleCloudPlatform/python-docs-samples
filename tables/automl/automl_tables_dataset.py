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


def create_dataset(project_id, compute_region, dataset_name):
    """Create a dataset."""
    # [START automl_tables_create_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_name = 'DATASET_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Set dataset name and metadata of the dataset.
    my_dataset = {
        "display_name": dataset_name,
        "tables_dataset_metadata": {}
    }

    # Create a dataset with the dataset metadata in the region.
    dataset = client.create_dataset(project_location, my_dataset)

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


def list_datasets(project_id, compute_region, filter_=None):
    """List all datasets."""
    # [START automl_tables_list_datasets]
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
        # Display the dataset information.
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        metadata = dataset.tables_dataset_metadata
        print("Dataset primary table spec id: {}".format(
            metadata.primary_table_spec_id))
        print("Dataset target column spec id: {}".format(
            metadata.target_column_spec_id))
        print("Dataset target column spec id: {}".format(
            metadata.target_column_spec_id))
        print("Dataset weight column spec id: {}".format(
            metadata.weight_column_spec_id))
        print("Dataset ml use column spec id: {}".format(
            metadata.ml_use_column_spec_id))
        print("Dataset example count: {}".format(dataset.example_count))
        print("Dataset create time:")
        print("\tseconds: {}".format(dataset.create_time.seconds))
        print("\tnanos: {}".format(dataset.create_time.nanos))
        print("\n")

    # [END automl_tables_list_datasets]


def list_table_specs(project_id, compute_region, dataset_id, filter_=None):
    """List all table specs."""
    # [START automl_tables_list_specs]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # List all the table specs in the dataset by applying filter.
    response = client.list_table_specs(dataset_full_id, filter_)

    print("List of table specs:")
    for table_spec in response:
        # Display the table_spec information.
        print("Table spec name: {}".format(table_spec.name))
        print("Table spec id: {}".format(table_spec.name.split("/")[-1]))
        print("Table spec time column spec id: {}".format(
            table_spec.time_column_spec_id))
        print("Table spec row count: {}".format(table_spec.row_count))
        print("Table spec column count: {}".format(table_spec.column_count))

    # [END automl_tables_list_specs]


def list_column_specs(project_id,
                      compute_region,
                      dataset_id,
                      table_spec_id,
                      filter_=None):
    """List all column specs."""
    # [START automl_tables_list_column_specs]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # table_spec_id = 'TABLE_SPEC_ID_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the table_spec.
    table_spec_full_id = client.table_spec_path(
        project_id, compute_region, dataset_id, table_spec_id
    )

    # List all the column specs in the table spec by applying filter.
    response = client.list_column_specs(table_spec_full_id, filter_)

    print("List of column specs:")
    for column_spec in response:
        # Display the column_spec information.
        print("Column spec name: {}".format(column_spec.name))
        print("Column spec id: {}".format(column_spec.name.split("/")[-1]))
        print("Column spec display name: {}".format(column_spec.display_name))
        print("Column spec data type: {}".format(column_spec.data_type))

    # [END automl_tables_list_column_specs]


def get_dataset(project_id, compute_region, dataset_id):
    """Get the dataset."""
    # [START automl_tables_get_dataset]
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

    # Get complete detail of the dataset.
    dataset = client.get_dataset(dataset_full_id)

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

    # [END automl_tables_get_dataset]


def get_table_spec(project_id, compute_region, dataset_id, table_spec_id):
    """Get the table spec."""
    # [START automl_tables_get_table_spec]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # table_spec_id = 'TABLE_SPEC_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the table spec.
    table_spec_full_id = client.table_spec_path(
        project_id, compute_region, dataset_id, table_spec_id
    )

    # Get complete detail of the table spec.
    table_spec = client.get_table_spec(table_spec_full_id)

    # Display the table spec information.
    print("Table spec name: {}".format(table_spec.name))
    print("Table spec id: {}".format(table_spec.name.split("/")[-1]))
    print("Table spec time column spec id: {}".format(
        table_spec.time_column_spec_id))
    print("Table spec row count: {}".format(table_spec.row_count))
    print("Table spec column count: {}".format(table_spec.column_count))

    # [END automl_tables_get_table_spec]


def get_column_spec(project_id,
                    compute_region,
                    dataset_id,
                    table_spec_id,
                    column_spec_id):
    """Get the column spec."""
    # [START automl_tables_get_column_spec]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # table_spec_id = 'TABLE_SPEC_ID_HERE'
    # column_spec_id = 'COLUMN_SPEC_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the column spec.
    column_spec_full_id = client.column_spec_path(
        project_id, compute_region, dataset_id, table_spec_id, column_spec_id
    )

    # Get complete detail of the column spec.
    column_spec = client.get_column_spec(column_spec_full_id)

    # Display the column spec information.
    print("Column spec name: {}".format(column_spec.name))
    print("Column spec id: {}".format(column_spec.name.split("/")[-1]))
    print("Column spec display name: {}".format(column_spec.display_name))
    print("Column spec data type: {}".format(column_spec.data_type))
    print("Column spec data stats: {}".format(column_spec.data_stats))
    print("Column spec top correlated columns\n")
    for column_correlation in column_spec.top_correlated_columns:
        print(column_correlation)

    # [END automl_tables_get_column_spec]


def import_data(project_id, compute_region, dataset_id, path):
    """Import structured data."""
    # [START automl_tables_import_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # path = 'gs://path/to/file.csv' or 'bq://project_id.dataset_id.table_id'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    if path.startswith('bq'):
        input_config = {"bigquery_source": {"input_uri": path}}
    else:    
        # Get the multiple Google Cloud Storage URIs.
        input_uris = path.split(",")
        input_config = {"gcs_source": {"input_uris": input_uris}}

    # Import data from the input URI.
    response = client.import_data(dataset_full_id, input_config)

    print("Processing import...")
    # synchronous check of operation status.
    print("Data imported. {}".format(response.result()))

    # [END automl_tables_import_data]


def export_data(project_id, compute_region, dataset_id, gcs_uri):
    """Export a dataset to a Google Cloud Storage bucket."""
    # [START automl_tables_export_data]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # output_uri: 'gs://location/to/export/data'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Set the output URI
    output_config = {"gcs_destination": {"output_uri_prefix": gcs_uri}}

    # Export the dataset to the output URI.
    response = client.export_data(dataset_full_id, output_config)

    print("Processing export...")
    # synchronous check of operation status.
    print("Data exported. {}".format(response.result()))

    # [END automl_tables_export_data]


def update_dataset(project_id,
                   compute_region,
                   dataset_id,
                   target_column_spec_id=None,
                   weight_column_spec_id=None,
                   ml_use_column_spec_id=None):
    """Update dataset."""
    # [START automl_tables_update_dataset]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # target_column_spec_id = 'TARGET_COLUMN_SPEC_ID_HERE' or None if unchanged
    # weight_column_spec_id = 'WEIGHT_COLUMN_SPEC_ID_HERE' or None if unchanged
    # ml_use_column_spec_id = 'ML_USE_COLUMN_SPEC_ID_HERE' or None if unchanged

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(
        project_id, compute_region, dataset_id
    )

    # Set the target, weight, and ml use columns in the tables dataset metadata.
    tables_dataset_metadata = {}
    if target_column_spec_id:
        tables_dataset_metadata['target_column_spec_id'] = target_column_spec_id
    if weight_column_spec_id:
        tables_dataset_metadata['weight_column_spec_id'] = weight_column_spec_id
    if ml_use_column_spec_id:
        tables_dataset_metadata['ml_use_column_spec_id'] = ml_use_column_spec_id

    # Set the updated tables dataset metadata in the dataset.
    my_dataset = {
        'name': dataset_full_id,
        'tables_dataset_metadata': tables_dataset_metadata,
    }

    # Update the dataset.
    response = client.update_dataset(my_dataset)

    # synchronous check of operation status.
    print("Dataset updated. {}".format(response))
    # [END automl_tables_update_dataset]


def update_table_spec(project_id,
                      compute_region,
                      dataset_id,
                      table_spec_id,
                      time_column_spec_id):
    """Update table spec."""
    # [START automl_tables_update_table_spec]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_spec_id = 'DATASET_ID_HERE'
    # table_spec_id = 'TABLE_SPEC_ID_HERE'
    # time_column_spec_id = 'TIME_COLUMN_SPEC_ID_HERE' or None if unchanged

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the table spec.
    table_spec_full_id = client.table_spec_path(
        project_id, compute_region, dataset_id, table_spec_id
    )

    # Set the updated time column in the table spec.
    my_table_spec = {
        'name': table_spec_full_id,
        'time_column_spec_id': time_column_spec_id
    }

    # Update the table spec.
    response = client.update_table_spec(my_table_spec)

    # synchronous check of operation status.
    print("Table spec updated. {}".format(response))
    # [END automl_tables_update_table_spec]


def update_column_spec(project_id,
                       compute_region,
                       dataset_id,
                       table_spec_id,
                       column_spec_id,
                       type_code,
                       nullable=None):
    """Update column spec."""
    # [START automl_tables_update_column_spec]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_spec_id = 'DATASET_ID_HERE'
    # table_spec_id = 'TABLE_SPEC_ID_HERE'
    # column_spec_id = 'COLUMN_SPEC_ID_HERE'
    # type_code = 'TYPE_CODE_HERE'
    # nullable = 'NULLABLE_HERE' or None if unchanged

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the column spec.
    column_spec_full_id = client.column_spec_path(
        project_id, compute_region, dataset_id, table_spec_id, column_spec_id
    )

    # Set type code and nullable in data_type.
    data_type = {'type_code': type_code}
    if nullable is not None:
        data_type['nullable'] = nullable

    # Set the updated data_type in the column_spec.
    my_column_spec = {
        'name': column_spec_full_id,
        'data_type': data_type,
    }

    # Update the column spec.
    response = client.update_column_spec(my_column_spec)

    # synchronous check of operation status.
    print("Table spec updated. {}".format(response))
    # [END automl_tables_update_column_spec]


def delete_dataset(project_id, compute_region, dataset_id):
    """Delete a dataset"""
    # [START automl_tables_delete_dataset]
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
    list_table_specs_parser.add_argument("--dataset_id")
    list_table_specs_parser.add_argument("--filter_")

    list_column_specs_parser = subparsers.add_parser(
        "list_column_specs", help=list_column_specs.__doc__
    )
    list_column_specs_parser.add_argument("--dataset_id")
    list_column_specs_parser.add_argument("--table_spec_id")
    list_column_specs_parser.add_argument("--filter_")

    get_dataset_parser = subparsers.add_parser(
        "get_dataset", help=get_dataset.__doc__
    )
    get_dataset_parser.add_argument("--dataset_id")

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
    import_data_parser.add_argument("--dataset_id")
    import_data_parser.add_argument("--path")

    export_data_parser = subparsers.add_parser(
        "export_data", help=export_data.__doc__
    )
    export_data_parser.add_argument("--dataset_id")
    export_data_parser.add_argument("--gcs_uri")

    update_dataset_parser = subparsers.add_parser(
        "update_dataset", help=update_dataset.__doc__
    )
    update_dataset_parser.add_argument("--dataset_id")
    update_dataset_parser.add_argument("--target_column_spec_id")
    update_dataset_parser.add_argument("--weight_column_spec_id")
    update_dataset_parser.add_argument("--ml_use_column_spec_id")

    update_table_spec_parser = subparsers.add_parser(
        "update_table_spec", help=update_table_spec.__doc__
    )
    update_table_spec_parser.add_argument("--dataset_id")
    update_table_spec_parser.add_argument("--table_spec_id")
    update_table_spec_parser.add_argument("--time_column_spec_id")

    update_column_spec_parser = subparsers.add_parser(
        "update_column_spec", help=update_column_spec.__doc__
    )
    update_column_spec_parser.add_argument("--dataset_id")
    update_column_spec_parser.add_argument("--column_spec_id")
    update_column_spec_parser.add_argument("--table_spec_id")
    update_column_spec_parser.add_argument("--type_code")
    update_column_spec_parser.add_argument("--nullable", type=bool)

    delete_dataset_parser = subparsers.add_parser(
        "delete_dataset", help=delete_dataset.__doc__
    )
    delete_dataset_parser.add_argument("--dataset_id")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()
    if args.command == "create_dataset":
        create_dataset(project_id, compute_region, args.dataset_name)
    if args.command == "list_datasets":
        list_datasets(project_id, compute_region, args.filter_)
    if args.command == "list_table_specs":
        list_table_specs(project_id,
                         compute_region,
                         args.dataset_id,
                         args.filter_)
    if args.command == "list_column_specs":
        list_column_specs(project_id,
                         compute_region,
                         args.dataset_id,
                         args.table_spec_id,
                         args.filter_)
    if args.command == "get_dataset":
        get_dataset(project_id, compute_region, args.dataset_id)
    if args.command == "get_table_spec":
        get_table_spec(project_id,
                       compute_region,
                       args.dataset_id,
                       args.table_spec_id)
    if args.command == "get_column_spec":
        get_column_spec(project_id,
                        compute_region,
                        args.dataset_id,
                        args.table_spec_id,
                        args.column_spec_id)
    if args.command == "import_data":
        import_data(project_id, compute_region, args.dataset_id, args.path)
    if args.command == "export_data":
        export_data(project_id, compute_region, args.dataset_id, args.gcs_uri)
    if args.command == "update_dataset":
        update_dataset(project_id,
                       compute_region,
                       args.dataset_id,
                       args.target_column_spec_id,
                       args.weight_column_spec_id, 
                       args.ml_use_column_spec_id)
    if args.command == "update_table_spec":
        update_table_spec(project_id,
                          compute_region,
                          args.dataset_id,
                          args.table_spec_id, 
                          args.time_column_spec_id)
    if args.command == "update_column_spec":
        update_column_spec(project_id,
                           compute_region,
                           args.dataset_id,
                           args.table_spec_id,
                           args.column_spec_id,
                           args.type_code, 
                           args.nullable)
    if args.command == "delete_dataset":
        delete_dataset(project_id, compute_region, args.dataset_id)

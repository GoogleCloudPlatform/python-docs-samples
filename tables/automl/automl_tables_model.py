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

"""This application demonstrates how to perform basic operations on model
with the Google AutoML Tables API.

For more information, the documentation at
https://cloud.google.com/automl-tables/docs.
"""

import argparse
import os


def create_model(project_id,
                 compute_region,
                 dataset_id,
                 model_name,
                 train_budget_milli_node_hours,
                 optimization_objective=None,
                 input_feature_column_specs=None):
    """Create a model."""
    # [START automl_tables_create_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # model_name = 'MODEL_NAME_HERE'
    # train_budget_milli_node_hours = 'TRAIN_BUDGET_MILLI_NODE_HOURS_HERE'
    # optimization_objective = 'OPTIMIZATION_OBJECTIVE_HEREs'
    #    or None if unspecified
    # input_feature_column_specs = 'INPUT_FEATURE_COLUMN_SPECS_HERE'
    #    or None if unspecified

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Sets an (optional) maximum train time, 1000 = 1 hour.
    tables_model_metadata = {}
    if train_budget_milli_node_hours:
        tables_model_metadata.update(
            {'train_budget_milli_node_hours': train_budget_milli_node_hours}
        )

    # Set the columns to use for training, defaults to all but the target and
    # ml use columns if unspecified. Expects a list of column specs, not ids.
    if input_feature_column_specs:
        tables_model_metadata.update(
            {'input_feature_column_specs': input_feature_column_specs}
        )

    # Set model name, dataset source, and metadata.
    my_model = {
        "display_name": model_name,
        "dataset_id": dataset_id,
        "tables_model_metadata": tables_model_metadata,
    }

    # Create a model with the model metadata in the region.
    response = client.create_model(project_location, my_model)

    print("Training model...")
    print("Training operation name: {}".format(response.operation.name))
    print("Training completed: {}".format(response.result()))

    # [END automl_tables_create_model]


def get_operation_status(operation_full_id):
    """Get operation status."""
    # [START automl_tables_get_operation_status]
    # TODO(developer): Uncomment and set the following variables
    # operation_full_id =
    #   'projects/<projectId>/locations/<region>/operations/<operationId>'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the latest state of a long-running operation.
    response = client.transport._operations_client.get_operation(
        operation_full_id
    )

    print("Operation status: {}".format(response))

    # [END automl_tables_get_operation_status]


def list_models(project_id, compute_region, filter_=None):
    """List all models."""
    # [START automl_tables_list_models]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # filter_ = 'DATASET_ID_HERE'

    from google.cloud import automl_v1beta1 as automl
    from google.cloud.automl_v1beta1 import enums

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # List all the models available in the region by applying filter.
    response = client.list_models(project_location, filter_)

    print("List of models:")
    for model in response:
        # Retrieve deployment state.
        if model.deployment_state == enums.Model.DeploymentState.DEPLOYED:
            deployment_state = "deployed"
        else:
            deployment_state = "undeployed"

        # Display the model information.
        print("Model name: {}".format(model.name))
        print("Model id: {}".format(model.name.split("/")[-1]))
        print("Model display name: {}".format(model.display_name))
        metadata = model.tables_model_metadata
        print("Target column display name: {}".format(
            metadata.target_column_spec.display_name))
        print("Training budget in node milli hours: {}".format(
            metadata.train_budget_milli_node_hours))
        print("Training cost in node milli hours: {}".format(
            metadata.train_cost_milli_node_hours))
        print("Model create time:")
        print("\tseconds: {}".format(model.create_time.seconds))
        print("\tnanos: {}".format(model.create_time.nanos))
        print("Model deployment state: {}".format(deployment_state))
        print("\n")

    # [END automl_tables_list_models]


def get_model(project_id, compute_region, model_id):
    """Get model details."""
    # [START automl_tables_get_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'

    from google.cloud import automl_v1beta1 as automl
    from google.cloud.automl_v1beta1 import enums

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # Get complete detail of the model.
    model = client.get_model(model_full_id)

    # Retrieve deployment state.
    if model.deployment_state == enums.Model.DeploymentState.DEPLOYED:
        deployment_state = "deployed"
    else:
        deployment_state = "undeployed"

    # Display the model information.
    print("Model name: {}".format(model.name))
    print("Model id: {}".format(model.name.split("/")[-1]))
    print("Model display name: {}".format(model.display_name))
    print("Model metadata:")
    print(model.tables_model_metadata)
    print("Model create time:")
    print("\tseconds: {}".format(model.create_time.seconds))
    print("\tnanos: {}".format(model.create_time.nanos))
    print("Model deployment state: {}".format(deployment_state))

    # [END automl_tables_get_model]


def list_model_evaluations(project_id, compute_region, model_id, filter_=None):
    """List model evaluations."""
    # [START automl_tables_list_model_evaluations]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # List all the model evaluations in the model by applying filter.
    response = client.list_model_evaluations(model_full_id, filter_)

    print("List of model evaluations:")
    for evaluation in response:
        print("Model evaluation name: {}".format(evaluation.name))
        print("Model evaluation id: {}".format(evaluation.name.split("/")[-1]))
        print("Model evaluation example count: {}".format(
            evaluation.evaluated_example_count))
        print("Model evaluation time:")
        print("\tseconds: {}".format(evaluation.create_time.seconds))
        print("\tnanos: {}".format(evaluation.create_time.nanos))
        print("\n")
    # [END automl_tables_list_model_evaluations]


def get_model_evaluation(
    project_id, compute_region, model_id, model_evaluation_id
):
    """Get model evaluation."""
    # [START automl_tables_get_model_evaluation]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # model_evaluation_id = 'MODEL_EVALUATION_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model evaluation.
    model_evaluation_full_id = client.model_evaluation_path(
        project_id, compute_region, model_id, model_evaluation_id
    )

    # Get complete detail of the model evaluation.
    response = client.get_model_evaluation(model_evaluation_full_id)

    print(response)

    # [END automl_tables_get_model_evaluation]


def display_evaluation(project_id, compute_region, model_id, filter_=None):
    """Display evaluation."""
    # [START automl_tables_display_evaluation]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # filter_ = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # List all the model evaluations in the model by applying filter.
    response = client.list_model_evaluations(model_full_id, filter_)

    # Iterate through the results.
    for evaluation in response:
        # There is evaluation for each class in a model and for overall model.
        # Get only the evaluation of overall model.
        if not evaluation.annotation_spec_id:
            model_evaluation_id = evaluation.name.split("/")[-1]

    # Resource name for the model evaluation.
    model_evaluation_full_id = client.model_evaluation_path(
        project_id, compute_region, model_id, model_evaluation_id
    )

    # Get a model evaluation.
    model_evaluation = client.get_model_evaluation(model_evaluation_full_id)

    classification_metrics = model_evaluation.classification_evaluation_metrics
    if str(classification_metrics):
        confidence_metrics = classification_metrics.confidence_metrics_entry

        # Showing model score based on threshold of 0.5
        print("Model classification metrics (threshold at 0.5):")
        for confidence_metrics_entry in confidence_metrics:
            if confidence_metrics_entry.confidence_threshold == 0.5:
                print(
                    "Model Precision: {}%".format(
                        round(confidence_metrics_entry.precision * 100, 2)
                    )
                )
                print(
                    "Model Recall: {}%".format(
                        round(confidence_metrics_entry.recall * 100, 2)
                    )
                )
                print(
                    "Model F1 score: {}%".format(
                        round(confidence_metrics_entry.f1_score * 100, 2)
                    )
                )
        print("Model AUPRC: {}".format(classification_metrics.au_prc))
        print("Model AUROC: {}".format(classification_metrics.au_roc))
        print("Model log loss: {}".format(classification_metrics.log_loss))

    regression_metrics = model_evaluation.regression_evaluation_metrics
    if str(regression_metrics):
        print("Model regression metrics:")
        print("Model RMSE: {}".format(regression_metrics.root_mean_squared_error))
        print("Model MAE: {}".format(regression_metrics.mean_absolute_error))
        print("Model MAPE: {}".format(
            regression_metrics.mean_absolute_percentage_error))
        print("Model R^2: {}".format(regression_metrics.r_squared))

    # [END automl_tables_display_evaluation]



def deploy_model(project_id, compute_region, model_id):
    """Deploy model."""
    # [START automl_tables_deploy_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # Deploy model
    response = client.deploy_model(model_full_id)

    print("Model deployed.")

    # [END automl_tables_deploy_model]



def undeploy_model(project_id, compute_region, model_id):
    """Undeploy model."""
    # [START automl_tables_undeploy_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # Deploy model
    response = client.undeploy_model(model_full_id)

    print("Model undeployed.")

    # [END automl_tables_undeploy_model]


def delete_model(project_id, compute_region, model_id):
    """Delete a model."""
    # [START automl_tables_delete_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # Delete a model.
    response = client.delete_model(model_full_id)

    # synchronous check of operation status.
    print("Model deleted. {}".format(response.result()))

    # [END automl_tables_delete_model]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    create_model_parser = subparsers.add_parser(
        "create_model", help=create_model.__doc__
    )
    create_model_parser.add_argument("--dataset_id")
    create_model_parser.add_argument("--model_name")
    create_model_parser.add_argument(
        "--train_budget_milli_node_hours", type=int,
    )
    create_model_parser.add_argument("--optimization_objective")

    get_operation_status_parser = subparsers.add_parser(
        "get_operation_status", help=get_operation_status.__doc__
    )
    get_operation_status_parser.add_argument("--operation_full_id")

    list_models_parser = subparsers.add_parser(
        "list_models", help=list_models.__doc__
    )
    list_models_parser.add_argument("--filter_")

    get_model_parser = subparsers.add_parser(
        "get_model", help=get_model.__doc__
    )
    get_model_parser.add_argument("--model_id")

    list_model_evaluations_parser = subparsers.add_parser(
        "list_model_evaluations", help=list_model_evaluations.__doc__
    )
    list_model_evaluations_parser.add_argument("--model_id")
    list_model_evaluations_parser.add_argument("--filter_")

    get_model_evaluation_parser = subparsers.add_parser(
        "get_model_evaluation", help=get_model_evaluation.__doc__
    )
    get_model_evaluation_parser.add_argument("--model_id")
    get_model_evaluation_parser.add_argument("--model_evaluation_id")

    display_evaluation_parser = subparsers.add_parser(
        "display_evaluation", help=display_evaluation.__doc__
    )
    display_evaluation_parser.add_argument("--model_id")
    display_evaluation_parser.add_argument("--filter_")

    deploy_model_parser = subparsers.add_parser(
        "deploy_model", help=deploy_model.__doc__
    )
    deploy_model_parser.add_argument("--model_id")

    undeploy_model_parser = subparsers.add_parser(
        "undeploy_model", help=undeploy_model.__doc__
    )
    undeploy_model_parser.add_argument("--model_id")

    delete_model_parser = subparsers.add_parser(
        "delete_model", help=delete_model.__doc__
    )
    delete_model_parser.add_argument("--model_id")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "create_model":
        create_model(
            project_id,
            compute_region,
            args.dataset_id,
            args.model_name,
            args.train_budget_milli_node_hours,
            # Input columns are omitted here as argparse does not support
            # column spec objects, but it is still included in function def.
        )
    if args.command == "get_operation_status":
        get_operation_status(args.operation_full_id)
    if args.command == "list_models":
        list_models(project_id, compute_region, args.filter_)
    if args.command == "get_model":
        get_model(project_id, compute_region, args.model_id)
    if args.command == "list_model_evaluations":
        list_model_evaluations(
            project_id, compute_region, args.model_id, args.filter_
        )
    if args.command == "get_model_evaluation":
        get_model_evaluation(
            project_id, compute_region, args.model_id, args.model_evaluation_id
        )
    if args.command == "display_evaluation":
        display_evaluation(
            project_id, compute_region, args.model_id, args.filter_
        )
    if args.command == "deploy_model":
        deploy_model(project_id, compute_region, args.model_id)
    if args.command == "undeploy_model":
        undeploy_model(project_id, compute_region, args.model_id)
    if args.command == "delete_model":
        delete_model(project_id, compute_region, args.model_id)

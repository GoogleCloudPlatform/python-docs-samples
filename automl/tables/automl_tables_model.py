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


def create_model(
    project_id,
    compute_region,
    dataset_display_name,
    model_display_name,
    train_budget_milli_node_hours,
    include_column_spec_names=None,
    exclude_column_spec_names=None,
):
    """Create a model."""
    # [START automl_tables_create_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_display_name = 'DATASET_DISPLAY_NAME_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # train_budget_milli_node_hours = 'TRAIN_BUDGET_MILLI_NODE_HOURS_HERE'
    # include_column_spec_names = 'INCLUDE_COLUMN_SPEC_NAMES_HERE'
    #    or None if unspecified
    # exclude_column_spec_names = 'EXCLUDE_COLUMN_SPEC_NAMES_HERE'
    #    or None if unspecified

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Create a model with the model metadata in the region.
    response = client.create_model(
        model_display_name,
        train_budget_milli_node_hours=train_budget_milli_node_hours,
        dataset_display_name=dataset_display_name,
        include_column_spec_names=include_column_spec_names,
        exclude_column_spec_names=exclude_column_spec_names,
    )

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

    client = automl.TablesClient()

    # Get the latest state of a long-running operation.
    op = client.auto_ml_client._transport.operations_client.get_operation(
        operation_full_id
    )

    print("Operation status: {}".format(op))

    # [END automl_tables_get_operation_status]


def list_models(project_id, compute_region, filter=None):
    """List all models."""
    result = []
    # [START automl_tables_list_models]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # filter = 'DATASET_DISPLAY_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # List all the models available in the region by applying filter.
    response = client.list_models(filter=filter)

    print("List of models:")
    for model in response:
        # Retrieve deployment state.
        if model.deployment_state == automl.Model.DeploymentState.DEPLOYED:
            deployment_state = "deployed"
        else:
            deployment_state = "undeployed"

        # Display the model information.
        print("Model name: {}".format(model.name))
        print("Model id: {}".format(model.name.split("/")[-1]))
        print("Model display name: {}".format(model.display_name))
        metadata = model.tables_model_metadata
        print(
            "Target column display name: {}".format(
                metadata.target_column_spec.display_name
            )
        )
        print(
            "Training budget in node milli hours: {}".format(
                metadata.train_budget_milli_node_hours
            )
        )
        print(
            "Training cost in node milli hours: {}".format(
                metadata.train_cost_milli_node_hours
            )
        )
        print("Model create time: {}".format(model.create_time))
        print("Model deployment state: {}".format(deployment_state))
        print("\n")

        # [END automl_tables_list_models]
        result.append(model)

    return result


def get_model(project_id, compute_region, model_display_name):
    """Get model details."""
    # [START automl_tables_get_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Get complete detail of the model.
    model = client.get_model(model_display_name=model_display_name)

    # Retrieve deployment state.
    if model.deployment_state == automl.Model.DeploymentState.DEPLOYED:
        deployment_state = "deployed"
    else:
        deployment_state = "undeployed"

    # get features of top importance
    feat_list = [
        (column.feature_importance, column.column_display_name)
        for column in model.tables_model_metadata.tables_model_column_info
    ]
    feat_list.sort(reverse=True)
    if len(feat_list) < 10:
        feat_to_show = len(feat_list)
    else:
        feat_to_show = 10

    # Display the model information.
    print("Model name: {}".format(model.name))
    print("Model id: {}".format(model.name.split("/")[-1]))
    print("Model display name: {}".format(model.display_name))
    print("Features of top importance:")
    for feat in feat_list[:feat_to_show]:
        print(feat)
    print("Model create time: {}".format(model.create_time))
    print("Model deployment state: {}".format(deployment_state))

    # [END automl_tables_get_model]

    return model


def list_model_evaluations(
    project_id, compute_region, model_display_name, filter=None
):

    """List model evaluations."""
    result = []
    # [START automl_tables_list_model_evaluations]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # filter = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # List all the model evaluations in the model by applying filter.
    response = client.list_model_evaluations(
        model_display_name=model_display_name, filter=filter
    )

    print("List of model evaluations:")
    for evaluation in response:
        print("Model evaluation name: {}".format(evaluation.name))
        print("Model evaluation id: {}".format(evaluation.name.split("/")[-1]))
        print(
            "Model evaluation example count: {}".format(
                evaluation.evaluated_example_count
            )
        )
        print("Model evaluation time: {}".format(evaluation.create_time))
        print("\n")
        # [END automl_tables_list_model_evaluations]
        result.append(evaluation)

    return result


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

    client = automl.TablesClient()

    # Get the full path of the model evaluation.
    model_path = client.auto_ml_client.model_path(
        project_id, compute_region, model_id
    )
    model_evaluation_full_id = f"{model_path}/modelEvaluations/{model_evaluation_id}"

    # Get complete detail of the model evaluation.
    response = client.get_model_evaluation(
        model_evaluation_name=model_evaluation_full_id
    )

    print(response)
    # [END automl_tables_get_model_evaluation]
    return response


def display_evaluation(
    project_id, compute_region, model_display_name, filter=None
):
    """Display evaluation."""
    # [START automl_tables_display_evaluation]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # filter = 'filter expression here'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # List all the model evaluations in the model by applying filter.
    response = client.list_model_evaluations(
        model_display_name=model_display_name, filter=filter
    )

    # Iterate through the results.
    for evaluation in response:
        # There is evaluation for each class in a model and for overall model.
        # Get only the evaluation of overall model.
        if not evaluation.annotation_spec_id:
            model_evaluation_name = evaluation.name
            break

    # Get a model evaluation.
    model_evaluation = client.get_model_evaluation(
        model_evaluation_name=model_evaluation_name
    )

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
        print(
            "Model RMSE: {}".format(regression_metrics.root_mean_squared_error)
        )
        print("Model MAE: {}".format(regression_metrics.mean_absolute_error))
        print(
            "Model MAPE: {}".format(
                regression_metrics.mean_absolute_percentage_error
            )
        )
        print("Model R^2: {}".format(regression_metrics.r_squared))

    # [END automl_tables_display_evaluation]


def deploy_model(project_id, compute_region, model_display_name):
    """Deploy model."""
    # [START automl_tables_deploy_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Deploy model
    response = client.deploy_model(model_display_name=model_display_name)

    # synchronous check of operation status.
    print("Model deployed. {}".format(response.result()))

    # [END automl_tables_deploy_model]


def undeploy_model(project_id, compute_region, model_display_name):
    """Undeploy model."""
    # [START automl_tables_undeploy_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Undeploy model
    response = client.undeploy_model(model_display_name=model_display_name)

    # synchronous check of operation status.
    print("Model undeployed. {}".format(response.result()))

    # [END automl_tables_undeploy_model]


def delete_model(project_id, compute_region, model_display_name):
    """Delete a model."""
    # [START automl_tables_delete_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Undeploy model
    response = client.delete_model(model_display_name=model_display_name)

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
    create_model_parser.add_argument("--dataset_display_name")
    create_model_parser.add_argument("--model_display_name")
    create_model_parser.add_argument(
        "--train_budget_milli_node_hours", type=int
    )

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
    get_model_parser.add_argument("--model_display_name")

    list_model_evaluations_parser = subparsers.add_parser(
        "list_model_evaluations", help=list_model_evaluations.__doc__
    )
    list_model_evaluations_parser.add_argument("--model_display_name")
    list_model_evaluations_parser.add_argument("--filter_")

    get_model_evaluation_parser = subparsers.add_parser(
        "get_model_evaluation", help=get_model_evaluation.__doc__
    )
    get_model_evaluation_parser.add_argument("--model_id")
    get_model_evaluation_parser.add_argument("--model_evaluation_id")

    display_evaluation_parser = subparsers.add_parser(
        "display_evaluation", help=display_evaluation.__doc__
    )
    display_evaluation_parser.add_argument("--model_display_name")
    display_evaluation_parser.add_argument("--filter_")

    deploy_model_parser = subparsers.add_parser(
        "deploy_model", help=deploy_model.__doc__
    )
    deploy_model_parser.add_argument("--model_display_name")

    undeploy_model_parser = subparsers.add_parser(
        "undeploy_model", help=undeploy_model.__doc__
    )
    undeploy_model_parser.add_argument("--model_display_name")

    delete_model_parser = subparsers.add_parser(
        "delete_model", help=delete_model.__doc__
    )
    delete_model_parser.add_argument("--model_display_name")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "create_model":
        create_model(
            project_id,
            compute_region,
            args.dataset_display_name,
            args.model_display_name,
            args.train_budget_milli_node_hours,
            # Input columns are omitted here as argparse does not support
            # column spec objects, but it is still included in function def.
        )
    if args.command == "get_operation_status":
        get_operation_status(args.operation_full_id)
    if args.command == "list_models":
        list_models(project_id, compute_region, args.filter_)
    if args.command == "get_model":
        get_model(project_id, compute_region, args.model_display_name)
    if args.command == "list_model_evaluations":
        list_model_evaluations(
            project_id, compute_region, args.model_display_name, args.filter_
        )
    if args.command == "get_model_evaluation":
        get_model_evaluation(
            project_id,
            compute_region,
            args.model_display_name,
            args.model_evaluation_id,
        )
    if args.command == "display_evaluation":
        display_evaluation(
            project_id, compute_region, args.model_display_name, args.filter_
        )
    if args.command == "deploy_model":
        deploy_model(project_id, compute_region, args.model_display_name)
    if args.command == "undeploy_model":
        undeploy_model(project_id, compute_region, args.model_display_name)
    if args.command == "delete_model":
        delete_model(project_id, compute_region, args.model_display_name)

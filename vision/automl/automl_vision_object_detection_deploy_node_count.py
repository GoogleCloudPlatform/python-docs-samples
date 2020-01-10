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


import argparse


def deploy_model_node_count(project_id, model_id):
    """Deploy a model."""
    # [START automl_vision_object_detection_deploy_model_node_count]
    from google.cloud import automl_v1beta1 as automl

    # project_id = 'YOUR_PROJECT_ID'
    # model_name = 'YOUR_MODEL_ID'

    client = automl.AutoMlClient()

    # The full path to your model
    full_model_id = client.model_path(project_id, 'us-central1', model_id)

    # Set how many nodes the model is deployed on
    model_deployment_metadata = (
        automl.types.ImageObjectDetectionModelDeploymentMetadata(node_count=2))

    # Deploy the model
    response = client.deploy_model(full_model_id, model_deployment_metadata)

    print(u'Model deployment on 2 nodes finished'.format(response.result()))
    # [END automl_vision_object_detection_deploy_model_node_count]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--project-id',
        help='YOUR_PROJECT_ID',
        required=True)
    parser.add_argument(
        '--model-id',
        help='YOUR_MODEL_ID',
        required=True)

    args = parser.parse_args()

    deploy_model_node_count(args.project_id, args.model_id)

# Copyright 2020 Google LLC
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


def deploy_model(project_id, model_id):
    """Deploy a model with a specified node count."""
    # [START automl_vision_object_detection_deploy_model_node_count]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # model_id = "YOUR_MODEL_ID"

    client = automl.AutoMlClient()
    # Get the full path of the model.
    model_full_id = client.model_path(project_id, "us-central1", model_id)

    # node count determines the number of nodes to deploy the model on.
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#imageobjectdetectionmodeldeploymentmetadata
    metadata = automl.ImageObjectDetectionModelDeploymentMetadata(node_count=2)

    request = automl.DeployModelRequest(
        name=model_full_id,
        image_object_detection_model_deployment_metadata=metadata,
    )
    response = client.deploy_model(request=request)

    print(f"Model deployment finished. {response.result()}")
    # [END automl_vision_object_detection_deploy_model_node_count]

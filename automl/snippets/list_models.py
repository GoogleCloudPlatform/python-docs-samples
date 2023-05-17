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


def list_models(project_id):
    """List models."""
    # [START automl_list_models]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"

    client = automl.AutoMlClient()
    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"

    request = automl.ListModelsRequest(parent=project_location, filter="")
    response = client.list_models(request=request)

    print("List of models:")
    for model in response:
        # Display the model information.
        if model.deployment_state == automl.Model.DeploymentState.DEPLOYED:
            deployment_state = "deployed"
        else:
            deployment_state = "undeployed"

        print(f"Model name: {model.name}")
        print("Model id: {}".format(model.name.split("/")[-1]))
        print(f"Model display name: {model.display_name}")
        print(f"Model create time: {model.create_time}")
        print(f"Model deployment state: {deployment_state}")
    # [END automl_list_models]

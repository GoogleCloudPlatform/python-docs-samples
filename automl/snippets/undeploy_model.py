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


def undeploy_model(project_id, model_id):
    """Undeploy a model."""
    # [START automl_undeploy_model]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # model_id = "YOUR_MODEL_ID"

    client = automl.AutoMlClient()
    # Get the full path of the model.
    model_full_id = client.model_path(project_id, "us-central1", model_id)
    response = client.undeploy_model(name=model_full_id)

    print("Model undeployment finished. {}".format(response.result()))
    # [END automl_undeploy_model]

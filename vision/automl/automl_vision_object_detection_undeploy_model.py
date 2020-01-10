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


def undeploy_model(project_id, model_id):
    """Undeploy a model."""
    # [START automl_vision_object_detection_undeploy_model]
    from google.cloud import automl_v1beta1 as automl

    # project_id = 'YOUR_PROJECT_ID'
    # model_name = 'YOUR_MODEL_ID'

    client = automl.AutoMlClient()

    # The full path to your model
    full_model_id = client.model_path(project_id, 'us-central1', model_id)

    # Undeploy the model
    response = client.undeploy_model(full_model_id)

    print(u'Model undeploy finished'.format(response.result()))
    # [END automl_vision_object_detection_undeploy_model]


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

    undeploy_model(args.project_id, args.model_id)

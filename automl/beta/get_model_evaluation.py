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


def get_model_evaluation(project_id, model_id, model_evaluation_id):
    """Get model evaluation."""
    # [START automl_video_classification_get_model_evaluation_beta]
    # [START automl_video_object_tracking_get_model_evaluation_beta]
    from google.cloud import automl_v1beta1 as automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # model_id = "YOUR_MODEL_ID"
    # model_evaluation_id = "YOUR_MODEL_EVALUATION_ID"

    client = automl.AutoMlClient()
    # Get the full path of the model evaluation.
    model_path = client.model_path(project_id, "us-central1", model_id)
    model_evaluation_full_id = f"{model_path}/modelEvaluations/{model_evaluation_id}"

    # Get complete detail of the model evaluation.
    response = client.get_model_evaluation(name=model_evaluation_full_id)

    print("Model evaluation name: {}".format(response.name))
    print("Model annotation spec id: {}".format(response.annotation_spec_id))
    print("Create Time: {}".format(response.create_time))
    print(
        "Evaluation example count: {}".format(response.evaluated_example_count)
    )

    # [END automl_video_object_tracking_get_model_evaluation_beta]

    print(
        "Classification model evaluation metrics: {}".format(
            response.classification_evaluation_metrics
        )
    )
    # [END automl_video_classification_get_model_evaluation_beta]

    # [START automl_video_object_tracking_get_model_evaluation_beta]
    print(
        "Video object tracking model evaluation metrics: {}".format(
            response.video_object_tracking_evaluation_metrics
        )
    )
    # [END automl_video_object_tracking_get_model_evaluation_beta]

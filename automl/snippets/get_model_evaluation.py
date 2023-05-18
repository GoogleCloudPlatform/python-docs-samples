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


def get_model_evaluation(project_id, model_id, model_evaluation_id):
    """Get model evaluation."""
    # [START automl_language_entity_extraction_get_model_evaluation]
    # [START automl_language_sentiment_analysis_get_model_evaluation]
    # [START automl_language_text_classification_get_model_evaluation]
    # [START automl_translate_get_model_evaluation]
    # [START automl_vision_classification_get_model_evaluation]
    # [START automl_vision_object_detection_get_model_evaluation]
    from google.cloud import automl

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

    print(f"Model evaluation name: {response.name}")
    print(f"Model annotation spec id: {response.annotation_spec_id}")
    print(f"Create Time: {response.create_time}")
    print(f"Evaluation example count: {response.evaluated_example_count}")
    # [END automl_language_sentiment_analysis_get_model_evaluation]
    # [END automl_language_text_classification_get_model_evaluation]
    # [END automl_translate_get_model_evaluation]
    # [END automl_vision_classification_get_model_evaluation]
    # [END automl_vision_object_detection_get_model_evaluation]
    print(
        "Entity extraction model evaluation metrics: {}".format(
            response.text_extraction_evaluation_metrics
        )
    )
    # [END automl_language_entity_extraction_get_model_evaluation]

    # [START automl_language_sentiment_analysis_get_model_evaluation]
    print(
        "Sentiment analysis model evaluation metrics: {}".format(
            response.text_sentiment_evaluation_metrics
        )
    )
    # [END automl_language_sentiment_analysis_get_model_evaluation]

    # [START automl_language_text_classification_get_model_evaluation]
    # [START automl_vision_classification_get_model_evaluation]
    print(
        "Classification model evaluation metrics: {}".format(
            response.classification_evaluation_metrics
        )
    )
    # [END automl_language_text_classification_get_model_evaluation]
    # [END automl_vision_classification_get_model_evaluation]

    # [START automl_translate_get_model_evaluation]
    print(
        "Translation model evaluation metrics: {}".format(
            response.translation_evaluation_metrics
        )
    )
    # [END automl_translate_get_model_evaluation]

    # [START automl_vision_object_detection_get_model_evaluation]
    print(
        "Object detection model evaluation metrics: {}".format(
            response.image_object_detection_evaluation_metrics
        )
    )
    # [END automl_vision_object_detection_get_model_evaluation]

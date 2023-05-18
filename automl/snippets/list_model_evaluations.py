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


def list_model_evaluations(project_id, model_id):
    """List model evaluations."""
    # [START automl_language_entity_extraction_list_model_evaluations]
    # [START automl_language_sentiment_analysis_list_model_evaluations]
    # [START automl_language_text_classification_list_model_evaluations]
    # [START automl_translate_list_model_evaluations]
    # [START automl_vision_classification_list_model_evaluations]
    # [START automl_vision_object_detection_list_model_evaluations]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # model_id = "YOUR_MODEL_ID"

    client = automl.AutoMlClient()
    # Get the full path of the model.
    model_full_id = client.model_path(project_id, "us-central1", model_id)

    print("List of model evaluations:")
    for evaluation in client.list_model_evaluations(parent=model_full_id, filter=""):
        print(f"Model evaluation name: {evaluation.name}")
        print(f"Model annotation spec id: {evaluation.annotation_spec_id}")
        print(f"Create Time: {evaluation.create_time}")
        print(f"Evaluation example count: {evaluation.evaluated_example_count}")
        # [END automl_language_sentiment_analysis_list_model_evaluations]
        # [END automl_language_text_classification_list_model_evaluations]
        # [END automl_translate_list_model_evaluations]
        # [END automl_vision_classification_list_model_evaluations]
        # [END automl_vision_object_detection_list_model_evaluations]
        print(
            "Entity extraction model evaluation metrics: {}".format(
                evaluation.text_extraction_evaluation_metrics
            )
        )
        # [END automl_language_entity_extraction_list_model_evaluations]

        # [START automl_language_sentiment_analysis_list_model_evaluations]
        print(
            "Sentiment analysis model evaluation metrics: {}".format(
                evaluation.text_sentiment_evaluation_metrics
            )
        )
        # [END automl_language_sentiment_analysis_list_model_evaluations]

        # [START automl_language_text_classification_list_model_evaluations]
        # [START automl_vision_classification_list_model_evaluations]
        print(
            "Classification model evaluation metrics: {}".format(
                evaluation.classification_evaluation_metrics
            )
        )
        # [END automl_language_text_classification_list_model_evaluations]
        # [END automl_vision_classification_list_model_evaluations]

        # [START automl_translate_list_model_evaluations]
        print(
            "Translation model evaluation metrics: {}".format(
                evaluation.translation_evaluation_metrics
            )
        )
        # [END automl_translate_list_model_evaluations]

        # [START automl_vision_object_detection_list_model_evaluations]
        print(
            "Object detection model evaluation metrics: {}\n\n".format(
                evaluation.image_object_detection_evaluation_metrics
            )
        )
        # [END automl_vision_object_detection_list_model_evaluations]

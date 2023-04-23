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


def get_dataset(project_id, dataset_id):
    """Get a dataset."""
    # [START automl_language_entity_extraction_get_dataset]
    # [START automl_language_sentiment_analysis_get_dataset]
    # [START automl_language_text_classification_get_dataset]
    # [START automl_translate_get_dataset]
    # [START automl_vision_classification_get_dataset]
    # [START automl_vision_object_detection_get_dataset]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # dataset_id = "YOUR_DATASET_ID"

    client = automl.AutoMlClient()
    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(project_id, "us-central1", dataset_id)
    dataset = client.get_dataset(name=dataset_full_id)

    # Display the dataset information
    print(f"Dataset name: {dataset.name}")
    print("Dataset id: {}".format(dataset.name.split("/")[-1]))
    print(f"Dataset display name: {dataset.display_name}")
    print(f"Dataset create time: {dataset.create_time}")
    # [END automl_language_sentiment_analysis_get_dataset]
    # [END automl_language_text_classification_get_dataset]
    # [END automl_translate_get_dataset]
    # [END automl_vision_classification_get_dataset]
    # [END automl_vision_object_detection_get_dataset]
    print(
        "Text extraction dataset metadata: {}".format(
            dataset.text_extraction_dataset_metadata
        )
    )
    # [END automl_language_entity_extraction_get_dataset]

    # [START automl_language_sentiment_analysis_get_dataset]
    print(
        "Text sentiment dataset metadata: {}".format(
            dataset.text_sentiment_dataset_metadata
        )
    )
    # [END automl_language_sentiment_analysis_get_dataset]

    # [START automl_language_text_classification_get_dataset]
    print(
        "Text classification dataset metadata: {}".format(
            dataset.text_classification_dataset_metadata
        )
    )
    # [END automl_language_text_classification_get_dataset]

    # [START automl_translate_get_dataset]
    print("Translation dataset metadata:")
    print(
        "\tsource_language_code: {}".format(
            dataset.translation_dataset_metadata.source_language_code
        )
    )
    print(
        "\ttarget_language_code: {}".format(
            dataset.translation_dataset_metadata.target_language_code
        )
    )
    # [END automl_translate_get_dataset]

    # [START automl_vision_classification_get_dataset]
    print(
        "Image classification dataset metadata: {}".format(
            dataset.image_classification_dataset_metadata
        )
    )
    # [END automl_vision_classification_get_dataset]

    # [START automl_vision_object_detection_get_dataset]
    print(
        "Image object detection dataset metadata: {}".format(
            dataset.image_object_detection_dataset_metadata
        )
    )
    # [END automl_vision_object_detection_get_dataset]

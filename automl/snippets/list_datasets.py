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


def list_datasets(project_id):
    """List datasets."""
    # [START automl_language_entity_extraction_list_datasets]
    # [START automl_language_sentiment_analysis_list_datasets]
    # [START automl_language_text_classification_list_datasets]
    # [START automl_translate_list_datasets]
    # [START automl_vision_classification_list_datasets]
    # [START automl_vision_object_detection_list_datasets]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"

    client = automl.AutoMlClient()
    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"

    # List all the datasets available in the region.
    request = automl.ListDatasetsRequest(parent=project_location, filter="")
    response = client.list_datasets(request=request)

    print("List of datasets:")
    for dataset in response:
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        print("Dataset create time: {}".format(dataset.create_time))
        # [END automl_language_sentiment_analysis_list_datasets]
        # [END automl_language_text_classification_list_datasets]
        # [END automl_translate_list_datasets]
        # [END automl_vision_classification_list_datasets]
        # [END automl_vision_object_detection_list_datasets]
        print(
            "Text extraction dataset metadata: {}".format(
                dataset.text_extraction_dataset_metadata
            )
        )
        # [END automl_language_entity_extraction_list_datasets]

        # [START automl_language_sentiment_analysis_list_datasets]
        print(
            "Text sentiment dataset metadata: {}".format(
                dataset.text_sentiment_dataset_metadata
            )
        )
        # [END automl_language_sentiment_analysis_list_datasets]

        # [START automl_language_text_classification_list_datasets]
        print(
            "Text classification dataset metadata: {}".format(
                dataset.text_classification_dataset_metadata
            )
        )
        # [END automl_language_text_classification_list_datasets]

        # [START automl_translate_list_datasets]
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
        # [END automl_translate_list_datasets]

        # [START automl_vision_classification_list_datasets]
        print(
            "Image classification dataset metadata: {}".format(
                dataset.image_classification_dataset_metadata
            )
        )
        # [END automl_vision_classification_list_datasets]

        # [START automl_vision_object_detection_list_datasets]
        print(
            "Image object detection dataset metadata: {}".format(
                dataset.image_object_detection_dataset_metadata
            )
        )
        # [END automl_vision_object_detection_list_datasets]

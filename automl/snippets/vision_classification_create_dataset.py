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


def create_dataset(project_id, display_name):
    """Create a dataset."""
    # [START automl_vision_classification_create_dataset]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # display_name = "your_datasets_display_name"

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"
    # Specify the classification type
    # Types:
    # MultiLabel: Multiple labels are allowed for one example.
    # MultiClass: At most one label is allowed per example.
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#classificationtype
    metadata = automl.ImageClassificationDatasetMetadata(
        classification_type=automl.ClassificationType.MULTILABEL
    )
    dataset = automl.Dataset(
        display_name=display_name,
        image_classification_dataset_metadata=metadata,
    )

    # Create a dataset with the dataset metadata in the region.
    response = client.create_dataset(parent=project_location, dataset=dataset, timeout=300)

    created_dataset = response.result()

    # Display the dataset information
    print("Dataset name: {}".format(created_dataset.name))
    print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
    # [END automl_vision_classification_create_dataset]

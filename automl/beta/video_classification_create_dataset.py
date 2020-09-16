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


# [START automl_video_classification_create_dataset_beta]
from google.cloud import automl_v1beta1 as automl


def create_dataset(
    project_id="YOUR_PROJECT_ID", display_name="your_datasets_display_name"
):
    """Create a automl video classification dataset."""

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"
    metadata = automl.VideoClassificationDatasetMetadata()
    dataset = automl.Dataset(
        display_name=display_name,
        video_classification_dataset_metadata=metadata,
    )

    # Create a dataset with the dataset metadata in the region.
    created_dataset = client.create_dataset(parent=project_location, dataset=dataset)

    # Display the dataset information
    print("Dataset name: {}".format(created_dataset.name))

    # To get the dataset id, you have to parse it out of the `name` field.
    # As dataset Ids are required for other methods.
    # Name Form:
    #    `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}`
    print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
# [END automl_video_classification_create_dataset_beta]

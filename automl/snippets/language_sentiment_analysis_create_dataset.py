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
    # [START automl_language_sentiment_analysis_create_dataset]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # display_name = "YOUR_DATASET_NAME"

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"

    # Each dataset requires a sentiment score with a defined sentiment_max
    # value, for more information on TextSentimentDatasetMetadata, see:
    # https://cloud.google.com/natural-language/automl/docs/prepare#sentiment-analysis
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#textsentimentdatasetmetadata
    metadata = automl.TextSentimentDatasetMetadata(
        sentiment_max=4
    )  # Possible max sentiment score: 1-10

    dataset = automl.Dataset(
        display_name=display_name, text_sentiment_dataset_metadata=metadata
    )

    # Create a dataset with the dataset metadata in the region.
    response = client.create_dataset(parent=project_location, dataset=dataset)

    created_dataset = response.result()

    # Display the dataset information
    print("Dataset name: {}".format(created_dataset.name))
    print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
    # [END automl_language_sentiment_analysis_create_dataset]

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


def export_dataset(project_id, dataset_id, gcs_uri):
    """Export a dataset."""
    # [START automl_export_dataset]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # dataset_id = "YOUR_DATASET_ID"
    # gcs_uri = "gs://YOUR_BUCKET_ID/path/to/export/"

    client = automl.AutoMlClient()

    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(project_id, "us-central1", dataset_id)

    gcs_destination = automl.GcsDestination(output_uri_prefix=gcs_uri)
    output_config = automl.OutputConfig(gcs_destination=gcs_destination)

    response = client.export_data(name=dataset_full_id, output_config=output_config)
    print(f"Dataset exported. {response.result()}")
    # [END automl_export_dataset]

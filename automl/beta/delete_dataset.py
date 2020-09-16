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


# [START automl_delete_dataset_beta]
from google.cloud import automl_v1beta1 as automl


def delete_dataset(project_id="YOUR_PROJECT_ID", dataset_id="YOUR_DATASET_ID"):
    """Delete a dataset."""
    client = automl.AutoMlClient()
    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(
        project_id, "us-central1", dataset_id
    )
    response = client.delete_dataset(name=dataset_full_id)

    print("Dataset deleted. {}".format(response.result()))
# [END automl_delete_dataset_beta]

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

# [START automl_video_object_tracking_create_model_beta]
from google.cloud import automl_v1beta1 as automl


def create_model(
    project_id="YOUR_PROJECT_ID",
    dataset_id="YOUR_DATASET_ID",
    display_name="your_models_display_name",
):
    """Create a automl video classification model."""
    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform loacation.
    project_location = f"projects/{project_id}/locations/us-central1"
    # Leave model unset to use the default base model provided by Google
    metadata = automl.VideoObjectTrackingModelMetadata()
    model = automl.Model(
        display_name=display_name,
        dataset_id=dataset_id,
        video_object_tracking_model_metadata=metadata,
    )

    # Create a model with the model metadata in the region.
    response = client.create_model(parent=project_location, model=model)

    print(f"Training operation name: {response.operation.name}")
    print("Training started...")
# [END automl_video_object_tracking_create_model_beta]

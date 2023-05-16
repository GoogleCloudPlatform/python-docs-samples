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


def predict(project_id, model_id, file_path):
    """Predict."""
    # [START automl_vision_object_detection_predict]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"
    # model_id = "YOUR_MODEL_ID"
    # file_path = "path_to_local_file.jpg"

    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(project_id, "us-central1", model_id)

    # Read the file.
    with open(file_path, "rb") as content_file:
        content = content_file.read()

    image = automl.Image(image_bytes=content)
    payload = automl.ExamplePayload(image=image)

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
    params = {"score_threshold": "0.8"}

    request = automl.PredictRequest(name=model_full_id, payload=payload, params=params)

    response = prediction_client.predict(request=request)
    print("Prediction results:")
    for result in response.payload:
        print(f"Predicted class name: {result.display_name}")
        print(f"Predicted class score: {result.image_object_detection.score}")
        bounding_box = result.image_object_detection.bounding_box
        print("Normalized Vertices:")
        for vertex in bounding_box.normalized_vertices:
            print(f"\tX: {vertex.x}, Y: {vertex.y}")
    # [END automl_vision_object_detection_predict]

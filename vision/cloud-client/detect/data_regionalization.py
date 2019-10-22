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


def data_regionalization():
    """Set a regional data endpoint using data regionalization"""
    # [START vision_client_library]
    # [START vision_data_regionalization]
    from google.cloud import vision

    client_options = {'api_endpoint': 'us-vision.googleapis.com:443'}

    client = vision.ImageAnnotatorClient(client_options=client_options)
    # [END vision_data_regionalization]

    image_source = vision.types.ImageSource(
        image_uri='gs://cloud-samples-data/vision/label/setagaya.jpeg')

    image = vision.types.Image(source=image_source)

    response = client.label_detection(image=image)

    print('Labels:')
    for label in response.label_annotations:
        print(label.description)
    # [END vision_client_library]

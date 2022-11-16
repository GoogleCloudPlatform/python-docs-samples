# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def set_endpoint():
    """Change your endpoint"""
    # [START vision_set_endpoint]
    from google.cloud import vision

    client_options = {'api_endpoint': 'eu-vision.googleapis.com'}

    client = vision.ImageAnnotatorClient(client_options=client_options)
    # [END vision_set_endpoint]
    image_source = vision.ImageSource(
        image_uri='gs://cloud-samples-data/vision/text/screen.jpg')
    image = vision.Image(source=image_source)

    response = client.text_detection(image=image)

    print('Texts:')
    for text in response.text_annotations:
        print('{}'.format(text.description))

        vertices = ['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices]

        print('bounds: {}\n'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


if __name__ == '__main__':
    set_endpoint()

#!/usr/bin/env python

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

r"""This is an example to call REST API from TFServing docker containers.

Examples:
    python automl_vision_edge_container_predict.py \
    --image_file_path=./test.jpg --image_key=1 --port_number=8051

"""

import argparse

# [START automl_vision_edge_container_predict]

import base64
import io
import json
import requests


def container_predict(image_file_path, image_key, port_number=8501):
    """Sends a prediction request to TFServing docker container REST API.

    Args:
        image_file_path: Path to a local image for the prediction request.
        image_key: Your chosen string key to identify the given image.
        port_number: The port number on your device to accept REST API calls.
    Returns:
        The response of the prediction request.
    """

    with io.open(image_file_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # The example here only shows prediction with one image. You can extend it
    # to predict with a batch of images indicated by different keys, which can
    # make sure that the responses corresponding to the given image.
    instances = {
            'instances': [
                    {'image_bytes': {'b64': str(encoded_image)},
                     'key': image_key}
            ]
    }

    # This example shows sending requests in the same server that you start
    # docker containers. If you would like to send requests to other servers,
    # please change localhost to IP of other servers.
    url = 'http://localhost:{}/v1/models/default:predict'.format(port_number)

    response = requests.post(url, data=json.dumps(instances))
    print(response.json())
    # [END automl_vision_edge_container_predict]
    return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_file_path', type=str)
    parser.add_argument('--image_key', type=str, default='1')
    parser.add_argument('--port_number', type=int, default=8501)
    args = parser.parse_args()

    container_predict(args.image_file_path, args.image_key, args.port_number)


if __name__ == '__main__':
    main()

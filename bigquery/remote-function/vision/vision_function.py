# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bigquery_remote_function_vision]
import flask
import functions_framework
from google.cloud import vision_v1


@functions_framework.http
def label_detection(request: flask.Request) -> flask.Response:
    """BigQuery remote function to label input images.
    Args:
        request: HTTP request from BigQuery
        https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#input_format
    Returns:
        HTTP response to BigQuery
        https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#output_format
    """
    try:
        client = vision_v1.ImageAnnotatorClient()
        calls = request.get_json()['calls']
        replies = []
        for call in calls:
            results = client.label_detection(
                {'source': {'image_uri': call[0]}})
            replies.append(vision_v1.AnnotateImageResponse.to_dict(results))
        return flask.make_response(flask.jsonify({'replies': replies}))
    except Exception as e:
        return flask.make_response(flask.jsonify({'errorMessage': str(e)}), 400)
# [END bigquery_remote_function_vision]

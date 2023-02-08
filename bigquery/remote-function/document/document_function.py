# Copyright 2023 Google LLC
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

# [START bigquery_remote_function_document]
import urllib.request

import flask
import functions_framework
from google.cloud import documentai

_PROJECT_ID = "YOUR_PROJECT_ID"
_LOCATION = "us"
_PROCESSOR_ID = "YOUR_PROCESSOR_ID"


@functions_framework.http
def document_ocr(request: flask.Request) -> flask.Response:
    """BigQuery remote function to process document using OCR.

    Args:
        request: HTTP request from BigQuery
        https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#input_format

    Returns:
        HTTP response to BigQuery
        https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#output_format
    """
    try:
        client = documentai.DocumentProcessorServiceClient()
        processor_name = client.processor_path(
            _PROJECT_ID, _LOCATION, _PROCESSOR_ID)
        calls = request.get_json()['calls']
        replies = []
        for call in calls:
            content = urllib.request.urlopen(call[0]).read()
            content_type = call[1]
            results = client.process_document(
                {'name': processor_name, 'raw_document': {
                    'content': content, 'mime_type': content_type}})
            replies.append(results.document.text)
        return flask.make_response(flask.jsonify({'replies': replies}))
    except Exception as e:
        return flask.make_response(flask.jsonify({'errorMessage': str(e)}), 400)
# [END bigquery_remote_function_document]

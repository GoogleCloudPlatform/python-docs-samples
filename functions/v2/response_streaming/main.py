# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_response_streaming]
from flask import Response, stream_with_context

import functions_framework
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()


@functions_framework.http
def stream_big_query_output(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Example large query from public dataset
    query = """
    SELECT abstract
    FROM `bigquery-public-data.breathe.bioasq`
    LIMIT 1000
    """
    query_job = client.query(query)  # Make an API request.

    def generate():
        for row in query_job:
            yield row[0]

    return Response(stream_with_context(generate()))


# [END functions_response_streaming]

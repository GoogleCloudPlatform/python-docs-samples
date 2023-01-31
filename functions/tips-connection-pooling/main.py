# Copyright 2022 Google LLC
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

# [START functions_tips_connection_pooling]
import functions_framework
import requests

# Create a global HTTP session (which provides connection pooling)
session = requests.Session()


@functions_framework.http
def connection_pooling(request):
    """
    HTTP Cloud Function that uses a connection pool to make HTTP requests.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    # The URL to send the request to
    url = 'http://example.com'

    # Process the request
    response = session.get(url)
    response.raise_for_status()
    return 'Success!'
# [END functions_tips_connection_pooling]

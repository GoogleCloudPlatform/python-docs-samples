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


# [START functions_tips_gcp_apis]
import os

import functions_framework
from google.cloud import pubsub_v1


# Create a global Pub/Sub client to avoid unneeded network activity
pubsub = pubsub_v1.PublisherClient()


@functions_framework.http
def gcp_api_call(request):
    """
    HTTP Cloud Function that uses a cached client library instance to
    reduce the number of connections required per function invocation.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    """
    The `GCP_PROJECT` environment variable is set automatically in the Python 3.7 runtime.
    In later runtimes, it must be specified by the user upon function deployment.
    See this page for more information:
        https://cloud.google.com/functions/docs/configuring/env-var#python_37_and_go_111
    """
    project = os.getenv('GCP_PROJECT')
    request_json = request.get_json()

    topic_name = request_json['topic']
    topic_path = pubsub.topic_path(project, topic_name)

    # Process the request
    data = 'Test message'.encode('utf-8')
    pubsub.publish(topic_path, data=data)

    return '1 message published'
# [END functions_tips_gcp_apis]

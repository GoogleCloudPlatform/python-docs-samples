# Copyright 2018 Google LLC
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

# [START functions_tips_infinite_retries]
from datetime import datetime, timezone
# [END functions_tips_infinite_retries]

# [START functions_tips_gcp_apis]
import os
# [END functions_tips_gcp_apis]

# [START functions_tips_infinite_retries]
# The 'python-dateutil' package must be included in requirements.txt.
from dateutil import parser

# [END functions_tips_infinite_retries]

# [START functions_tips_retry]
from google.cloud import error_reporting
# [END functions_tips_retry]

# [START functions_tips_gcp_apis]
from google.cloud import pubsub_v1
# [END functions_tips_gcp_apis]

# [START functions_tips_connection_pooling]
import requests

# [END functions_tips_connection_pooling]

from functools import reduce  # noqa I100


# Placeholder
def file_wide_computation():
    return 1


# Placeholder
def function_specific_computation():
    return 1


def light_computation():
    numbers = list(range(1, 10))
    return reduce(lambda x, t: t + x, numbers)


def heavy_computation():
    # Multiplication is more computationally expensive than addition
    numbers = list(range(1, 10))
    return reduce(lambda x, t: t * x, numbers)


# [START cloudrun_tips_global_scope]
# [START run_tips_global_scope]
# Global (instance-wide) scope
# This computation runs at instance cold-start
instance_var = heavy_computation()


def scope_demo(request):
    """
    HTTP Cloud Function that declares a variable.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    function_var = light_computation()
    return 'Per instance: {}, per function: {}'.format(
        instance_var, function_var)
# [END run_tips_global_scope]
# [END cloudrun_tips_global_scope]


# [START functions_tips_lazy_globals]
# [START cloudrun_tips_global_lazy]
# [START run_tips_global_lazy]
# Always initialized (at cold-start)
non_lazy_global = file_wide_computation()

# Declared at cold-start, but only initialized if/when the function executes
lazy_global = None


def lazy_globals(request):
    """
    HTTP Cloud Function that uses lazily-initialized globals.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    global lazy_global, non_lazy_global

    # This value is initialized only if (and when) the function is called
    if not lazy_global:
        lazy_global = function_specific_computation()

    return 'Lazy: {}, non-lazy: {}.'.format(lazy_global, non_lazy_global)
# [END run_tips_global_lazy]
# [END cloudrun_tips_global_lazy]
# [END functions_tips_lazy_globals]


# [START functions_tips_connection_pooling]
# Create a global HTTP session (which provides connection pooling)
session = requests.Session()


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


# [START functions_tips_gcp_apis]

# Create a global Pub/Sub client to avoid unneeded network activity
pubsub = pubsub_v1.PublisherClient()


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

    project = os.getenv('GCP_PROJECT')
    request_json = request.get_json()

    topic_name = request_json['topic']
    topic_path = pubsub.topic_path(project, topic_name)

    # Process the request
    data = 'Test message'.encode('utf-8')
    pubsub.publish(topic_path, data=data)

    return '1 message published'
# [END functions_tips_gcp_apis]


# [START functions_tips_infinite_retries]
def avoid_infinite_retries(data, context):
    """Background Cloud Function that only executes within a certain
    time period after the triggering event.

    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): The event metadata.
    Returns:
        None; output is written to Stackdriver Logging
    """

    timestamp = context.timestamp

    event_time = parser.parse(timestamp)
    event_age = (datetime.now(timezone.utc) - event_time).total_seconds()
    event_age_ms = event_age * 1000

    # Ignore events that are too old
    max_age_ms = 10000
    if event_age_ms > max_age_ms:
        print('Dropped {} (age {}ms)'.format(context.event_id, event_age_ms))
        return 'Timeout'

    # Do what the function is supposed to do
    print('Processed {} (age {}ms)'.format(context.event_id, event_age_ms))
    return  # To retry the execution, raise an exception here
# [END functions_tips_infinite_retries]


# [START functions_tips_retry]
error_client = error_reporting.Client()


def retry_or_not(data, context):
    """Background Cloud Function that demonstrates how to toggle retries.

    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): The event metadata.
    Returns:
        None; output is written to Stackdriver Logging
    """

    # Retry based on a user-defined parameter
    try_again = data.data.get('retry') is not None

    try:
        raise RuntimeError('I failed you')
    except RuntimeError:
        error_client.report_exception()
        if try_again:
            raise  # Raise the exception and try again
        else:
            pass   # Swallow the exception and don't retry
# [END functions_tips_retry]

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
from datetime import datetime

# The 'python-dateutil' package must be included in requirements.txt.
from dateutil import parser

# [END functions_tips_infinite_retries]
# [START functions_tips_connection_pooling]
import requests

# [END functions_tips_connection_pooling]


# Placeholder
def file_wide_computation():
    return 1


# Placeholder
def function_specific_computation():
    return 1


# [START functions_tips_lazy_globals]
# Always initialized (at cold-start)
non_lazy_global = file_wide_computation()

# Declared at cold-start, but only initialized if/when the function executes
lazy_global = None


def lazy_globals(request):
    """
    HTTP Cloud Function that uses lazily-initialized globals.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>.
    """
    global lazy_global, non_lazy_global

    # This value is initialized only if (and when) the function is called
    if not lazy_global:
        lazy_global = function_specific_computation()

    return 'Lazy: {}, non-lazy: {}.'.format(lazy_global, non_lazy_global)
# [END functions_tips_lazy_globals]


# [START functions_tips_connection_pooling]
# Create a global HTTP session (which provides connection pooling)
session = requests.Session()


def connection_pooling(request):
    """
    HTTP Cloud Function that uses a connection pool to make HTTP requests.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>.
    """

    # The URL to send the request to
    url = 'http://example.com'

    # Process the request
    response = session.get(url)
    response.raise_for_status()
    return 'Success!'
# [END functions_tips_connection_pooling]


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

    timestamp = data.timestamp

    event_time = parser.parse(timestamp)
    event_age = (datetime.now() - event_time).total_seconds() * 1000

    # Ignore events that are too old
    max_age_ms = 10000
    if event_age > max_age_ms:
        print('Dropped {} (age {}ms)'.format(context.event_id, event_age))
        return 'Timeout'

    # Do what the function is supposed to do
    print('Processed {} (age {}ms)'.format(context.event_id, event_age))
    return
# [END functions_tips_infinite_retries]


# [START functions_tips_retry]
def retry_or_not(data, context):
    """Background Cloud Function that demonstrates how to toggle retries.

    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): The event metadata.
    Returns:
        None; output is written to Stackdriver Logging
    """

    from google import cloud
    error_client = cloud.error_reporting.Client()

    if data.data.get('retry'):
        try_again = True
    else:
        try_again = False

    try:
        raise RuntimeError('I failed you')
    except RuntimeError:
        error_client.report_exception()
        if try_again:
            raise  # Raise the exception and try again
        else:
            pass   # Swallow the exception and don't retry
# [END functions_tips_retry]

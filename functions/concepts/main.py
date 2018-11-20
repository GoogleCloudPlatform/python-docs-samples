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

import time


# [START functions_concepts_stateless]
# Global variable, modified within the function by using the global keyword.
count = 0


def statelessness(request):
    """
    HTTP Cloud Function that counts how many times it is executed
    within a specific instance.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    global count
    count += 1

    # Note: the total function invocation count across
    # all instances may not be equal to this value!
    return 'Instance execution count: {}'.format(count)
# [END functions_concepts_stateless]


# Placeholder
def heavy_computation():
    return time.time()


# Placeholder
def light_computation():
    return time.time()


# [START functions_tips_scopes]
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

    # Per-function scope
    # This computation runs every time this function is called
    function_var = light_computation()
    return 'Instance: {}; function: {}'.format(instance_var, function_var)
# [END functions_tips_scopes]


# [START functions_concepts_requests]
def make_request(request):
    """
    HTTP Cloud Function that makes another HTTP request.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    import requests

    # The URL to send the request to
    url = 'http://example.com'

    # Process the request
    response = requests.get(url)
    response.raise_for_status()
    return 'Success!'
# [END functions_concepts_requests]


# [START functions_concepts_after_timeout]
def timeout(request):
    print('Function running...')
    time.sleep(120)

    # May not execute if function's timeout is <2 minutes
    print('Function completed!')
    return 'Function completed!'
# [END functions_concepts_after_timeout]


# [START functions_concepts_filesystem]
def list_files(request):
    import os
    from os import path

    root = path.dirname(path.abspath(__file__))
    children = os.listdir(root)
    files = [c for c in children if path.isfile(path.join(root, c))]
    return 'Files: {}'.format(files)
# [END functions_concepts_filesystem]

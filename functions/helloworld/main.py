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

import sys

# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape

# [END functions_helloworld_http]
# [END functions_http_content]


# [START functions_tips_terminate]
# [START functions_helloworld_get]
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    return 'Hello World!'
# [END functions_helloworld_get]


# [START functions_helloworld_background]
def hello_background(data, context):
    """Background Cloud Function.
    Args:
         data (dict): The dictionary with data specific to the given event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    if data and 'name' in data:
        name = data['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)
# [END functions_helloworld_background]
# [END functions_tips_terminate]


# [START functions_helloworld_http]
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))
# [END functions_helloworld_http]


# [START functions_helloworld_pubsub]
def hello_pubsub(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    import base64

    if 'data' in data:
        name = base64.b64decode(data['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))
# [END functions_helloworld_pubsub]


# [START functions_helloworld_storage]
def hello_gcs(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions
         event metadata.
    """
    print("File: {}.".format(data['objectId']))
# [END functions_helloworld_storage]


# [START functions_http_content]
def hello_content(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data
    elif content_type == 'text/plain':
        name = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello {}!'.format(escape(name))
# [END functions_http_content]


# [START functions_http_methods]
def hello_method(request):
    """ Responds to a GET request with "Hello world!". Forbids a PUT request.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
         Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    from flask import abort

    if request.method == 'GET':
        return 'Hello World!'
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)
# [END functions_http_methods]


def hello_error_1(request):
    # [START functions_helloworld_error]
    # This WILL be reported to Stackdriver Error
    # Reporting, and WILL NOT show up in logs or
    # terminate the function.
    from google.cloud import error_reporting
    client = error_reporting.Client()

    try:
        raise RuntimeError('I failed you')
    except RuntimeError:
        client.report_exception()

    # This WILL be reported to Stackdriver Error Reporting,
    # and WILL terminate the function
    raise RuntimeError('I failed you')

    # [END functions_helloworld_error]


def hello_error_2(request):
    # [START functions_helloworld_error]
    # WILL NOT be reported to Stackdriver Error Reporting, but will show up
    # in logs
    import logging
    print(RuntimeError('I failed you (print to stdout)'))
    logging.warn(RuntimeError('I failed you (logging.warn)'))
    logging.error(RuntimeError('I failed you (logging.error)'))
    sys.stderr.write('I failed you (sys.stderr.write)\n')

    # This WILL be reported to Stackdriver Error Reporting
    from flask import abort
    return abort(500)
    # [END functions_helloworld_error]

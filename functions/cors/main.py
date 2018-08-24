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


# [START functions_cors]
def cors_enabled_function(request):
    # Set CORS headers for the preflight request
    # e.g. allows GETs from any origin with the Content-Type header
    # and cache preflight response for an 3600s
    preflight_request_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    # Send response to OPTIONS requests and terminate the function execution
    if request.method == 'OPTIONS':
        return ('', 204, preflight_request_headers)

    # Set CORS headers for the main request
    main_request_headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return ('Hello World!', 200, main_request_headers)
# [END functions_cors]


# [START functions_cors_authentication]
def cors_enabled_function_auth(request):
    # Set CORS headers for preflight requests
    # e.g. allows GETS from origin https://mydomain.com with Authorization
    # header
    preflight_request_headers = {
        'Access-Control-Allow-Origin': 'https://mydomain.com',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Authorization',
        'Access-Control-Max-Age': '3600',
        'Access-Control-Allow-Credentials': 'true'
    }

    # Send response to OPTIONS requests and terminate the function execution
    if request.method == 'OPTIONS':
        return ('', 204, preflight_request_headers)

    # Set CORS headers for main requests
    main_request_headers = {
        'Access-Control-Allow-Origin': 'https://mydomain.com',
        'Access-Control-Allow-Credentials': 'true'
    }

    return ('Hello World!', 200, main_request_headers)
# [END functions_cors_authentication]

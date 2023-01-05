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


# [START functions_tips_scopes]
# [START cloudrun_tips_global_scope]
import time

import functions_framework


# Placeholder
def heavy_computation():
    return time.time()


# Placeholder
def light_computation():
    return time.time()


# Global (instance-wide) scope
# This computation runs at instance cold-start
instance_var = heavy_computation()


@functions_framework.http
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
# [END cloudrun_tips_global_scope]

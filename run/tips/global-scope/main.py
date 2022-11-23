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

from functools import reduce  # noqa I100


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
    HTTP route that declares a variable.
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

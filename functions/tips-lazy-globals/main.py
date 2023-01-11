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

# [START functions_tips_lazy_globals]
# [START cloudrun_tips_global_lazy]
import functions_framework

# [END cloudrun_tips_global_lazy]
# [END functions_tips_lazy_globals]


# Placeholder
def file_wide_computation():
    return 1


# Placeholder
def function_specific_computation():
    return 1


# [START functions_tips_lazy_globals]
# [START cloudrun_tips_global_lazy]
# Always initialized (at cold-start)
non_lazy_global = file_wide_computation()

# Declared at cold-start, but only initialized if/when the function executes
lazy_global = None


@functions_framework.http
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
# [END cloudrun_tips_global_lazy]
# [END functions_tips_lazy_globals]

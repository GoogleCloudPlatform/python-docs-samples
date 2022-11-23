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


# [START functions_tips_retry]
from google.cloud import error_reporting


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

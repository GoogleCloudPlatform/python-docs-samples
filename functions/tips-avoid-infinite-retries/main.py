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

# [START functions_tips_infinite_retries]
from datetime import datetime, timezone

# The 'python-dateutil' package must be included in requirements.txt.
from dateutil import parser


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
        print(f'Dropped {context.event_id} (age {event_age_ms}ms)')
        return 'Timeout'

    # Do what the function is supposed to do
    print(f'Processed {context.event_id} (age {event_age_ms}ms)')
    return  # To retry the execution, raise an exception here
# [END functions_tips_infinite_retries]

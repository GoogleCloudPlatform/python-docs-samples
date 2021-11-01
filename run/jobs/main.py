# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import time
import os
import random

# Retrieve Job-defined env vars
TASK_NUM = os.getenv('TASK_NUM') or 0
ATTEMPT_NUM = os.getenv('ATTEMPT_NUM')
# Retrieve User-defined env vars
SLEEP_MS = os.getenv('SLEEP_MS')
FAIL_RATE = os.getenv('FAIL_RATE')

# Define main script
def main():
    print(f"Starting Task #{TASK_NUM}, Attempt #{ATTEMPT_NUM}...")
    # Simulate work
    if (SLEEP_MS):
        # Wait for a specific amount of time
        time.sleep(SLEEP_MS/1000)  # Convert to seconds

    # Simulate errors
    if (FAIL_RATE):
        random_failure(FAIL_RATE)

    print(f"Completed Task #{TASK_NUM}.")



# Throw an error based on fail rate
def random_failure(rate):
    rate = float(rate)
    if (rate == None or rate < 0 or rate > 1):
        print(f"Invalid FAIL_RATE env var value: {FAIL_RATE}. Must be a float between 0 and 1 inclusive.")
        return

    random_failure = random.random()
    if (random_failure < rate ):
        msg = f"Task #{TASK_NUM}, Attempt #{ATTEMPT_NUM} failed."
        print(json.dumps({'message': msg, 'severity': 'ERROR'}))
        raise Exception(msg)  # Fail job - will trigger retry


# Start script
if __name__ == '__main__':
    main()
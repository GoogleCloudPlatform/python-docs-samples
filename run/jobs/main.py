# Copyright 2022 Google LLC.
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

# [START cloudrun_jobs_quickstart]
import json
import os
import random
import sys
import time

# [START cloudrun_jobs_env_vars]
# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 0)
FAIL_RATE = os.getenv("FAIL_RATE", 0)
# [END cloudrun_jobs_env_vars]


# Define main script
def main(sleep_ms=0, fail_rate=0):
    print(f"Starting Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    # Simulate work by waiting for a specific amount of time
    time.sleep(float(sleep_ms) / 1000)  # Convert to seconds

    # Simulate errors
    random_failure(float(fail_rate))

    print(f"Completed Task #{TASK_INDEX}.")


# Throw an error based on fail rate
def random_failure(rate):
    if rate < 0 or rate > 1:
        # Return without retrying the Job Task
        print(
            f"Invalid FAIL_RATE env var value: {rate}. " +
            "Must be a float between 0 and 1 inclusive."
        )
        return

    random_failure = random.random()
    if random_failure < rate:
        raise Exception("Task failed.")


# Start script
if __name__ == "__main__":
    try:
        main(SLEEP_MS, FAIL_RATE)
    except Exception as err:
        message = f"Task #{TASK_INDEX}, " \
                  + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"

        print(json.dumps({"message": message, "severity": "ERROR"}))
        # [START cloudrun_jobs_exit_process]
        sys.exit(1)  # Retry Job Task by exiting the process
        # [END cloudrun_jobs_exit_process]
# [END cloudrun_jobs_quickstart]

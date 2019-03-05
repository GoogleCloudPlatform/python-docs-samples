#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""An example of starting https://cloud.google.com/profiler."""

# [START profiler_python_quickstart]
import googlecloudprofiler


def main():
    # Profiler initialization. It starts a daemon thread which continuously
    # collects and uploads profiles. Best done as early as possible.
    try:
        googlecloudprofiler.start(
            service='hello-profiler',
            service_version='1.0.1',
            # verbose is the logging level. 0-error, 1-warning, 2-info,
            # 3-debug. It defaults to 0 (error) if not set.
            verbose=3,
            # project_id must be set if not running on GCP.
            # project_id='my-project-id',
        )
    except (ValueError, NotImplementedError) as exc:
        print(exc)  # Handle errors here
# [END profiler_python_quickstart]
    busyloop()


# A loop function which spends 30% CPU time on loop3() and 70% CPU time
# on loop7().
def busyloop():
    while True:
        loop3()
        loop7()


def loop3():
    for _ in range(3):
        loop()


def loop7():
    for _ in range(7):
        loop()


def loop():
    for _ in range(10000):
        pass


if __name__ == '__main__':
    main()

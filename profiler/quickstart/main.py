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

if __name__ == '__main__':
    # Profiler initialization, best done as early as possible.
    try:
        googlecloudprofiler.start(
            service='service-name',
            service_version='version',
            verbose=3,
            # project_id must be set if not running on GCP.
            # project_id='my-project-id',
        )
    except (ValueError, NotImplementedError) as e:
        print(e)  # Handles errors here

# [END profiler_python_quickstart]
    while True:
        pass

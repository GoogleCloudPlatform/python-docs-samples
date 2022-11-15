#!/usr/bin/env python
#
# Copyright 2022 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START error_reporting_quickstart]
# [START error_reporting_setup_python]
def simulate_error():
    from google.cloud import error_reporting

    client = error_reporting.Client()
    try:
        # simulate calling a method that's not defined
        raise NameError
    except Exception:
        client.report_exception()
# [END error_reporting_setup_python]
# [END error_reporting_quickstart]


# [START error_reporting_manual]
# [START error_reporting_setup_python_manual]
def report_manual_error():
    from google.cloud import error_reporting

    client = error_reporting.Client()
    client.report("An error has occurred.")
# [END error_reporting_setup_python_manual]
# [END error_reporting_manual]


if __name__ == '__main__':
    simulate_error()
    report_manual_error()

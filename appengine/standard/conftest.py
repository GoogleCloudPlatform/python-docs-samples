# Copyright 2015 Google Inc.
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

import os

# Import py.test hooks and fixtures for App Engine
from appengine_helper import (
    login,
    pytest_configure,
    pytest_runtest_call,
    run_tasks,
    testbed,
)
import six

(login)
(pytest_configure)
(pytest_runtest_call)
(run_tasks)
(testbed)


def pytest_ignore_collect(path, config):
    """Skip App Engine tests in python 3 or if no SDK is available."""
    if "appengine/standard" in str(path):
        if six.PY3:
            return True
        if "GAE_SDK_PATH" not in os.environ:
            return True
    return False

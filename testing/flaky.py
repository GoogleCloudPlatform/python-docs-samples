# Copyright 2015, Google, Inc.
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

"""
Tools for dealing with flaky tests.
"""
from __future__ import absolute_import


from flaky import flaky
import gcloud
import pytest


def flaky_filter(e, *args):
    """Used by mark_flaky to retry on remote service errors."""
    exception_class, exception_instance, traceback = e
    return isinstance(
        exception_instance,
        (gcloud.exceptions.GCloudError,))


def mark_flaky(f):
    """Makes a test retry on remote service errors."""
    return flaky(max_runs=3, rerun_filter=flaky_filter)(
        pytest.mark.flaky(f))

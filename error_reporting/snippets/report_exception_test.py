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

import time

import google.auth
from google.cloud import errorreporting_v1beta1

import report_exception

PROJECT = google.auth.default()[1]


def test_error_sends(ess_client: errorreporting_v1beta1.ErrorStatsServiceClient):
    report_exception.report_exception()

    req = errorreporting_v1beta1.ListGroupStatsRequest()
    req.project_name = f"projects/{PROJECT}"
    time.sleep(30)  # waiting to make sure changes applied
    data = ess_client.list_group_stats(req)

    for group in data.error_group_stats:
        if "Something went wrong" in group.representative.message:
            break
    else:
        assert False


def test_manual_error_sends(ess_client: errorreporting_v1beta1.ErrorStatsServiceClient):
    report_exception.report_manual_error()

    req = errorreporting_v1beta1.ListGroupStatsRequest()
    req.project_name = f"projects/{PROJECT}"
    time.sleep(30)  # waiting to make sure changes applied
    data = ess_client.list_group_stats(req)

    for group in data.error_group_stats:
        if "An error has occurred." in group.representative.message:
            break
    else:
        assert False

# Copyright 2022 Google LLC
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
#

# flake8: noqa

import os

from documentai.snippets import cancel_operation_sample
from documentai.snippets import get_operation_sample
from documentai.snippets import list_operations_sample
from documentai.snippets import poll_operation_sample

from google.api_core.exceptions import FailedPrecondition
from google.api_core.exceptions import NotFound


def test_get_operation(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    operation_id = "10828996427112056798"
    operation_name = (
        f"projects/{project_id}/locations/{location}/operations/{operation_id}"
    )

    try:
        get_operation_sample.get_operation_sample(
            location=location, operation_name=operation_name
        )
    except NotFound as e:
        print(e.message)

    out, _ = capsys.readouterr()

    assert "operation" in out


def test_list_operations(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    operations_filter = "TYPE=BATCH_PROCESS_DOCUMENTS AND STATE=DONE"
    list_operations_sample.list_operations_sample(
        project_id=project_id, location=location, operations_filter=operations_filter
    )
    out, _ = capsys.readouterr()

    assert "operations" in out


def test_poll_operation(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    operation_id = "10828996427112056798"
    operation_name = (
        f"projects/{project_id}/locations/{location}/operations/{operation_id}"
    )

    try:
        poll_operation_sample.poll_operation_sample(
            location=location, operation_name=operation_name
        )
    except NotFound as e:
        print(e.message)

    out, _ = capsys.readouterr()

    assert "operation" in out


def test_cancel_operation(capsys):
    location = "us"
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    operation_id = "4311241022337572151"
    operation_name = (
        f"projects/{project_id}/locations/{location}/operations/{operation_id}"
    )
    try:
        cancel_operation_sample.cancel_operation_sample(
            location=location, operation_name=operation_name
        )
    except (FailedPrecondition, NotFound) as e:
        print(e.message)

    out, _ = capsys.readouterr()

    assert "Operation" in out

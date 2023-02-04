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

import re
import typing
import uuid

import google.auth

from create_certificate_template import create_certificate_template
from delete_certificate_template import delete_certificate_template
from list_certificate_templates import list_certificate_templates
from update_certificate_template import update_certificate_template

PROJECT = google.auth.default()[1]
LOCATION = "us-central1"
COMMON_NAME = "COMMON_NAME"
ORGANIZATION = "ORGANIZATION"
CA_DURATION = 1000000


def generate_name() -> str:
    return "i" + uuid.uuid4().hex[:10]


def test_create_delete_certificate_template(capsys: typing.Any) -> None:
    TEMPLATE_NAME = generate_name()

    create_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)
    delete_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)

    out, _ = capsys.readouterr()

    assert re.search(
        f'Operation result: name: "projects/{PROJECT}/locations/{LOCATION}/certificateTemplates/{TEMPLATE_NAME}"',
        out,
    )

    assert re.search(f"Deleted certificate template: {TEMPLATE_NAME}", out)


def test_list_certificate_templates(certificate_template, capsys: typing.Any) -> None:
    TEMPLATE_NAME = certificate_template

    list_certificate_templates(PROJECT, LOCATION)

    out, _ = capsys.readouterr()

    assert "Available certificate templates:" in out
    assert f"{TEMPLATE_NAME}\n" in out


def test_update_certificate_template(certificate_template, capsys: typing.Any) -> None:
    TEMPLATE_NAME = certificate_template

    update_certificate_template(PROJECT, LOCATION, TEMPLATE_NAME)

    out, _ = capsys.readouterr()

    assert "Successfully updated the certificate template!" in out

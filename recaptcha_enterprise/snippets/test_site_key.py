#!/usr/bin/env python
# Copyright 2021 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All Rights Reserved.


import os
import re

from _pytest.capture import CaptureFixture
import pytest

from create_site_key import create_site_key
from delete_site_key import delete_site_key
from get_metrics import get_metrics
from get_site_key import get_site_key
from list_site_keys import list_site_keys
from update_site_key import update_site_key

# TODO(developer): Replace these variables before running the sample.
GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
DOMAIN_NAME = "localhost"


@pytest.fixture(scope="module")
def recaptcha_site_key() -> str:
    recaptcha_site_key = create_site_key(
        project_id=GOOGLE_CLOUD_PROJECT, domain_name=DOMAIN_NAME
    )
    yield recaptcha_site_key
    delete_site_key(
        project_id=GOOGLE_CLOUD_PROJECT, recaptcha_site_key=recaptcha_site_key
    )


def test_create_site_key(recaptcha_site_key: str) -> None:
    assert len(recaptcha_site_key) != 0


def test_list_site_keys(capsys: CaptureFixture, recaptcha_site_key: str) -> None:
    list_site_keys(project_id=GOOGLE_CLOUD_PROJECT)
    out, _ = capsys.readouterr()
    assert re.search(f"keys/{recaptcha_site_key}", out)


def test_get_site_key(capsys: CaptureFixture, recaptcha_site_key: str) -> None:
    get_site_key(project_id=GOOGLE_CLOUD_PROJECT, recaptcha_site_key=recaptcha_site_key)
    out, _ = capsys.readouterr()
    assert re.search(f"Successfully obtained the key !.+{recaptcha_site_key}", out)


def test_update_site_key(capsys: CaptureFixture, recaptcha_site_key: str) -> None:
    update_site_key(
        project_id=GOOGLE_CLOUD_PROJECT,
        recaptcha_site_key=recaptcha_site_key,
        domain_name=DOMAIN_NAME,
    )
    out, _ = capsys.readouterr()
    assert re.search("reCAPTCHA Site key successfully updated ! ", out)


def test_get_metrics(capsys: CaptureFixture, recaptcha_site_key: str) -> None:
    get_metrics(project_id=GOOGLE_CLOUD_PROJECT, recaptcha_site_key=recaptcha_site_key)
    out, _ = capsys.readouterr()
    assert re.search(
        f"Retrieved the bucket count for score based key: {recaptcha_site_key}", out
    )

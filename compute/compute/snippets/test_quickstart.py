# Copyright 2021 Google LLC
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

from samples.snippets.quickstart import main

PROJECT = google.auth.default()[1]
INSTANCE_NAME = "i" + uuid.uuid4().hex[:10]
INSTANCE_ZONE = "europe-central2-b"


def test_main(capsys: typing.Any) -> None:
    main(PROJECT, INSTANCE_ZONE, INSTANCE_NAME)

    out, _ = capsys.readouterr()

    assert f"Instance {INSTANCE_NAME} created." in out
    assert re.search(f"Instances found in {INSTANCE_ZONE}:.+{INSTANCE_NAME}", out)
    assert re.search(f"zones/{INSTANCE_ZONE}:.+{INSTANCE_NAME}", out)
    assert f"Instance {INSTANCE_NAME} deleted." in out

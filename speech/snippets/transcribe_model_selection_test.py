# Copyright 2016 Google LLC
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

import os
import re

from google.api_core.retry import Retry
import pytest

import transcribe_model_selection

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_transcribe_model_selection_file(capsys: pytest.CaptureFixture) -> None:
    response = transcribe_model_selection.transcribe_model_selection()
    out, err = capsys.readouterr()

    assert re.search(r"the weather outside is sunny", out, re.DOTALL | re.I)
    assert response is not None


@Retry()
def test_transcribe_model_selection_gcs(capsys: pytest.CaptureFixture) -> None:
    response = transcribe_model_selection.transcribe_model_selection_gcs()
    out, err = capsys.readouterr()

    assert re.search(r"the weather outside is sunny", out, re.DOTALL | re.I)
    assert response is not None

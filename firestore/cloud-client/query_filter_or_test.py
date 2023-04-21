# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest

from google.cloud import firestore
from query_filter_or import query_or_composite_filter

os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture
def setup(autouse=True):
    client = firestore.Client(project=PROJECT_ID)
    cr = client.collection("knownUsers")
    td = [
        {"shortName": "aturing", "birthYear": 1912},
        {"shortName": "cbabbage", "birthYear": 1791},
        {"shortName": "ghopper", "birthYear": 1906},
        {"shortName": "alovelace", "birthYear": 1815},
    ]

    for d in td:
        cr.documents(d["shortName"]).set({"birthYear": d["birthYear"]})

    yield

    for d in td:
        cr.documents(d["shortName"]).delete()


def test_query_or_composite_filter(capsys):
    query_or_composite_filter(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert "aturing" in out

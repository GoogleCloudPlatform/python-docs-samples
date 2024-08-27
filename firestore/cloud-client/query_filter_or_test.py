# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff
import pytest

from query_filter_or import query_or_compound_filter
from query_filter_or import query_or_filter
import snippets_test

os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]
PROJECT_ID = os.environ["FIRESTORE_PROJECT"]


@pytest.fixture(scope="module")
def data():
    return {
        "San Francisco": {"capital": False, "population": 884_363, "state": "CA"},
        "Los Angeles": {"capital": False, "population": 3_976_000, "state": "CA"},
        "Sacramento": {"capital": True, "population": 508_529, "state": "CA"},
        "New York City": {"capital": False, "population": 8_336_817, "state": "NY"},
        "Seattle": {"capital": False, "population": 744_955, "state": "WA"},
        "Olympia": {"capital": True, "population": 52_555, "state": "WA"},
        "Phoenix": {"capital": True, "population": 1_445_632, "state": "AZ"},
    }


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def create_document(key, val, collection):
    collection.document(key).set(val)


def create_document_collection(data, collection):
    for key, val in data.items():
        create_document(key, val, collection)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def delete_document(key, collection):
    collection.document(key).delete()


def delete_document_collection(data, collection):
    for key in data:
        delete_document(key, collection)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def test_query_or_filter(capsys, data):
    client = snippets_test.TestFirestoreClient(
        project=PROJECT_ID, add_unique_string=False
    )
    collection = client.collection("cities")

    try:
        create_document_collection(data, collection)
        query_or_filter(client)
    finally:
        delete_document_collection(data, collection)

    out, _ = capsys.readouterr()
    for city in data:
        if data[city]["capital"] or data[city]["population"] > 1_000_000:
            assert city in out
        else:
            assert city not in out


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def test_query_or_compound_filter(capsys, data):
    client = snippets_test.TestFirestoreClient(
        project=PROJECT_ID, add_unique_string=False
    )
    collection = client.collection("cities")

    try:
        create_document_collection(data, collection)
        query_or_compound_filter(client)
    finally:
        delete_document_collection(data, collection)

    out, _ = capsys.readouterr()
    for city in data:
        if data[city]["state"] == "CA" and (
            data[city]["capital"] or data[city]["population"] > 1_000_000
        ):
            assert city in out
        else:
            assert city not in out

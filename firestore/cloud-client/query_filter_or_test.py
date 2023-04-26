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

from google.cloud import firestore

import backoff
import pytest

from query_filter_or import query_or_composite_filter

os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['FIRESTORE_PROJECT']
PROJECT_ID = os.environ['FIRESTORE_PROJECT']


@pytest.fixture(scope="module")
def data():
    return {
            u'aturing': {u'birthYear': 1912},
            u'cbabbage': {u'birthYear': 1791},
            u'ghopper': {u'birthYear': 1906},
            u'alovelace': {u'birthYear': 1815},
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
def test_query_or_composite_filter(capsys, data):
    client = firestore.Client(project=PROJECT_ID)
    collection = client.collection('users')

    try:
        create_document_collection(data, collection)
        query_or_composite_filter(PROJECT_ID)
    finally:
        delete_document_collection(data, collection)

    out, _ = capsys.readouterr()
    assert 'aturing' in out

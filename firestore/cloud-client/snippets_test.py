# Copyright 2017 Google, LLC.
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
import uuid

from google.cloud import firestore
import pytest

import snippets

os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['FIRESTORE_PROJECT']

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]


class TestFirestoreClient(firestore.Client):
    def __init__(self, *args, **kwargs):
        self._UNIQUE_STRING = UNIQUE_STRING
        self._super = super()
        self._super.__init__(*args, **kwargs)

    def collection(self, collection_name, *args, **kwargs):
        collection_name += f'-{self._UNIQUE_STRING}'
        return self._super.collection(collection_name, *args, **kwargs)


snippets.firestore.Client = TestFirestoreClient


@pytest.fixture
def db():
    yield snippets.firestore.Client()


def test_quickstart_new_instance():
    snippets.quickstart_new_instance()


def test_quickstart_add_data_two():
    snippets.quickstart_add_data_two()


def test_quickstart_get_collection():
    snippets.quickstart_get_collection()


def test_quickstart_add_data_one():
    snippets.quickstart_add_data_one()


def test_add_from_dict():
    snippets.add_from_dict()


def test_add_data_types():
    snippets.add_data_types()


def test_add_example_data():
    snippets.add_example_data()


def test_array_contains_any(db):
    query = snippets.array_contains_any_queries(db)

    expected = {'SF', 'LA', 'DC'}
    actual = {document.id for document in query.stream()}

    assert expected == actual


def test_query_filter_in_query_without_array(db):
    query = snippets.in_query_without_array(db)

    expected = {'SF', 'LA', 'DC', 'TOK'}
    actual = {document.id for document in query.stream()}

    assert expected == actual


def test_query_filter_in_query_with_array(db):
    query = snippets.in_query_with_array(db)

    expected = {'DC'}
    actual = {document.id for document in query.stream()}

    assert expected == actual


def test_add_custom_class_with_id():
    snippets.add_custom_class_with_id()


def test_add_data_with_id():
    snippets.add_data_with_id()


def test_add_custom_class_generated_id():
    snippets.add_custom_class_generated_id()


def test_add_new_doc():
    snippets.add_new_doc()


def test_get_simple_query():
    snippets.get_simple_query()


def test_array_contains_filter(capsys):
    snippets.array_contains_filter()
    out, _ = capsys.readouterr()
    assert 'SF' in out


def test_get_full_collection():
    snippets.get_full_collection()


def test_get_custom_class():
    snippets.get_custom_class()


def test_get_check_exists():
    snippets.get_check_exists()


def test_structure_subcollection_ref():
    snippets.structure_subcollection_ref()


def test_structure_collection_ref():
    snippets.structure_collection_ref()


def test_structure_doc_ref_alternate():
    snippets.structure_doc_ref_alternate()


def test_structure_doc_ref():
    snippets.structure_doc_ref()


def test_update_create_if_missing():
    snippets.update_create_if_missing()


def test_update_doc():
    snippets.update_doc()


def test_update_doc_array(capsys):
    snippets.update_doc_array()
    out, _ = capsys.readouterr()
    assert 'greater_virginia' in out


def test_update_multiple():
    snippets.update_multiple()


def test_update_server_timestamp(db):
    db.collection('objects').document('some-id').set({'timestamp': 0})
    snippets.update_server_timestamp()


def test_update_data_transaction(db):
    db.collection('cities').document('SF').set({'population': 1})
    snippets.update_data_transaction()


def test_update_data_transaction_result(db):
    db.collection('cities').document('SF').set({'population': 1})
    snippets.update_data_transaction_result()


def test_update_data_batch(db):
    db.collection('cities').document('SF').set({})
    db.collection('cities').document('LA').set({})
    snippets.update_data_batch()


def test_update_nested():
    snippets.update_nested()


def test_compound_query_example():
    snippets.compound_query_example()


def test_compound_query_valid_multi_clause():
    snippets.compound_query_valid_multi_clause()


def test_compound_query_simple():
    snippets.compound_query_simple()


def test_compound_query_invalid_multi_field():
    snippets.compound_query_invalid_multi_field()


def test_compound_query_single_clause():
    snippets.compound_query_single_clause()


def test_compound_query_valid_single_field():
    snippets.compound_query_valid_single_field()


def test_order_simple_limit():
    snippets.order_simple_limit()


def test_order_simple_limit_desc():
    snippets.order_simple_limit_desc()


def test_order_multiple():
    snippets.order_multiple()


def test_order_where_limit():
    snippets.order_where_limit()


def test_order_limit_to_last():
    snippets.order_limit_to_last()


def test_order_where_invalid():
    snippets.order_where_invalid()


def test_order_where_valid():
    snippets.order_where_valid()


def test_cursor_simple_start_at():
    snippets.cursor_simple_start_at()


def test_cursor_simple_end_at():
    snippets.cursor_simple_end_at()


def test_snapshot_cursors(capsys):
    snippets.snapshot_cursors()
    out, _ = capsys.readouterr()
    assert 'SF' in out
    assert 'TOK' in out
    assert 'BJ' in out


def test_cursor_paginate():
    snippets.cursor_paginate()


def test_cursor_multiple_conditions():
    snippets.cursor_multiple_conditions()


@pytest.mark.flaky(max_runs=3)
def test_listen_document(capsys):
    snippets.listen_document()
    out, _ = capsys.readouterr()
    assert 'Received document snapshot: SF' in out


@pytest.mark.flaky(max_runs=3)
def test_listen_multiple(capsys):
    snippets.listen_multiple()
    out, _ = capsys.readouterr()
    assert 'Current cities in California:' in out
    assert 'SF' in out


@pytest.mark.flaky(max_runs=3)
def test_listen_for_changes(capsys):
    snippets.listen_for_changes()
    out, _ = capsys.readouterr()
    assert 'New city: MTV' in out
    assert 'Modified city: MTV' in out
    assert 'Removed city: MTV' in out


def test_delete_single_doc():
    snippets.delete_single_doc()


def test_delete_field(db):
    db.collection('cities').document('BJ').set({'capital': True})
    snippets.delete_field()


def test_delete_full_collection():
    snippets.delete_full_collection()


@pytest.mark.skip(reason="Dependant on a composite index being created,"
                         "however creation of the index is dependent on"
                         "having the admin client and definition integrated"
                         "into the test setup")
# TODO: b/132092178
def test_collection_group_query(db):
    museum_docs = snippets.collection_group_query(db)
    names = {museum.name for museum in museum_docs}
    assert names == {'Legion of Honor', 'The Getty',
                     'National Air and Space Museum',
                     'National Museum of Nature and Science',
                     'Beijing Ancient Observatory'}


def test_list_document_subcollections():
    snippets.list_document_subcollections()


def test_create_and_build_bundle():
    bundle, buffer = snippets.create_and_build_bundle()
    assert "latest-stories-query" in bundle.named_queries


def test_regional_endpoint():
    snippets.regional_endpoint()

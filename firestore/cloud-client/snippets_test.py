# Copyright 2017, Google, Inc.
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

from google.cloud import firestore
import pytest

import snippets

os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['FIRESTORE_PROJECT']


@pytest.fixture
def db():
    yield firestore.Client()


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


def test_update_multiple():
    snippets.update_multiple()


def test_update_server_timestamp(db):
    db.collection(u'objects').document(u'some-id').set({'timestamp': 0})
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


def test_order_where_invalid():
    snippets.order_where_invalid()


def test_order_where_valid():
    snippets.order_where_valid()


def test_cursor_simple_start_at():
    snippets.cursor_simple_start_at()


def test_cursor_simple_end_at():
    snippets.cursor_simple_end_at()


def test_cursor_paginate():
    snippets.cursor_paginate()


def test_cursor_multiple_conditions():
    snippets.cursor_multiple_conditions()


def test_delete_single_doc():
    snippets.delete_single_doc()


def test_delete_field(db):
    db.collection('cities').document('Beijing').set({'capital': True})
    snippets.delete_field()


def test_delete_full_collection():
    snippets.delete_full_collection()

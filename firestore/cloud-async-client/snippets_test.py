# Copyright 2020 Google, Inc.
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

import os
import uuid

from google.cloud import firestore
import pytest

import snippets

os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]


class TestFirestoreAsyncClient(firestore.AsyncClient):
    def __init__(self, *args, **kwargs):
        self._UNIQUE_STRING = UNIQUE_STRING
        self._super = super()
        self._super.__init__(*args, **kwargs)

    def collection(self, collection_name, *args, **kwargs):
        collection_name += f"-{self._UNIQUE_STRING}"
        return self._super.collection(collection_name, *args, **kwargs)


snippets.firestore.AsyncClient = TestFirestoreAsyncClient
pytestmark = pytest.mark.asyncio


@pytest.fixture
def db():
    yield snippets.firestore.AsyncClient()


async def test_quickstart_new_instance():
    await snippets.quickstart_new_instance()


async def test_quickstart_add_data_two():
    await snippets.quickstart_add_data_two()


async def test_quickstart_get_collection():
    await snippets.quickstart_get_collection()


async def test_quickstart_add_data_one():
    await snippets.quickstart_add_data_one()


async def test_add_from_dict():
    await snippets.add_from_dict()


async def test_add_data_types():
    await snippets.add_data_types()


async def test_add_example_data():
    await snippets.add_example_data()


async def test_array_contains_any(db):
    query = await snippets.array_contains_any_queries(db)

    expected = {"SF", "LA", "DC"}
    actual = {document.id async for document in query.stream()}

    assert expected == actual


async def test_query_filter_in_query_without_array(db):
    query = await snippets.in_query_without_array(db)

    expected = {"SF", "LA", "DC", "TOK"}
    actual = {document.id async for document in query.stream()}

    assert expected == actual


async def test_query_filter_in_query_with_array(db):
    query = await snippets.in_query_with_array(db)

    expected = {"DC"}
    actual = {document.id async for document in query.stream()}

    assert expected == actual


async def test_add_custom_class_with_id():
    await snippets.add_custom_class_with_id()


async def test_add_data_with_id():
    await snippets.add_data_with_id()


async def test_add_custom_class_generated_id():
    await snippets.add_custom_class_generated_id()


async def test_add_new_doc():
    await snippets.add_new_doc()


async def test_get_simple_query():
    await snippets.get_simple_query()


async def test_array_contains_filter(capsys):
    await snippets.array_contains_filter()
    out, _ = capsys.readouterr()
    assert "SF" in out


async def test_get_full_collection():
    await snippets.get_full_collection()


async def test_get_custom_class():
    await snippets.get_custom_class()


async def test_get_check_exists():
    await snippets.get_check_exists()


async def test_structure_subcollection_ref():
    await snippets.structure_subcollection_ref()


async def test_structure_collection_ref():
    await snippets.structure_collection_ref()


async def test_structure_doc_ref_alternate():
    await snippets.structure_doc_ref_alternate()


async def test_structure_doc_ref():
    await snippets.structure_doc_ref()


async def test_update_create_if_missing():
    await snippets.update_create_if_missing()


async def test_update_doc():
    await snippets.update_doc()


async def test_update_doc_array(capsys):
    await snippets.update_doc_array()
    out, _ = capsys.readouterr()
    assert "greater_virginia" in out


async def test_update_multiple():
    await snippets.update_multiple()


async def test_update_server_timestamp(db):
    await db.collection("objects").document("some-id").set({"timestamp": 0})
    await snippets.update_server_timestamp()


async def test_update_data_transaction(db):
    await db.collection("cities").document("SF").set({"population": 1})
    await snippets.update_data_transaction()


async def test_update_data_transaction_result(db):
    await db.collection("cities").document("SF").set({"population": 1})
    await snippets.update_data_transaction_result()


async def test_update_data_batch(db):
    await db.collection("cities").document("SF").set({})
    await db.collection("cities").document("LA").set({})
    await snippets.update_data_batch()


async def test_update_nested():
    await snippets.update_nested()


async def test_compound_query_example():
    await snippets.compound_query_example()


async def test_compound_query_valid_multi_clause():
    await snippets.compound_query_valid_multi_clause()


async def test_compound_query_simple():
    await snippets.compound_query_simple()


async def test_compound_query_invalid_multi_field():
    await snippets.compound_query_invalid_multi_field()


async def test_compound_query_single_clause():
    await snippets.compound_query_single_clause()


async def test_compound_query_valid_single_field():
    await snippets.compound_query_valid_single_field()


async def test_order_simple_limit():
    await snippets.order_simple_limit()


async def test_order_simple_limit_desc():
    await snippets.order_simple_limit_desc()


async def test_order_multiple():
    await snippets.order_multiple()


async def test_order_where_limit():
    await snippets.order_where_limit()


async def test_order_limit_to_last():
    await snippets.order_limit_to_last()


async def test_order_where_invalid():
    await snippets.order_where_invalid()


async def test_order_where_valid():
    await snippets.order_where_valid()


async def test_cursor_simple_start_at():
    await snippets.cursor_simple_start_at()


async def test_cursor_simple_end_at():
    await snippets.cursor_simple_end_at()


async def test_snapshot_cursors(capsys):
    await snippets.snapshot_cursors()
    out, _ = capsys.readouterr()
    assert "SF" in out
    assert "TOK" in out
    assert "BJ" in out


async def test_cursor_paginate():
    await snippets.cursor_paginate()


async def test_cursor_multiple_conditions():
    await snippets.cursor_multiple_conditions()


async def test_delete_single_doc():
    await snippets.delete_single_doc()


async def test_delete_field(db):
    await db.collection("cities").document("BJ").set({"capital": True})
    await snippets.delete_field()


async def test_delete_full_collection():
    await snippets.delete_full_collection()


@pytest.mark.skip(
    reason="Dependant on a composite index being created,"
    "however creation of the index is dependent on"
    "having the admin client and definition integrated"
    "into the test setup"
)
# TODO: b/132092178
async def test_collection_group_query(db):
    museum_docs = await snippets.collection_group_query(db)
    names = {museum.name for museum in museum_docs}
    assert names == {
        "Legion of Honor",
        "The Getty",
        "National Air and Space Museum",
        "National Museum of Nature and Science",
        "Beijing Ancient Observatory",
    }


async def test_list_document_subcollections():
    await snippets.list_document_subcollections()

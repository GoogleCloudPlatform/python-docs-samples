# Copyright 2016 Google Inc. All rights reserved.
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


from google.appengine.api import search
import pytest

import snippets


@pytest.fixture
def search_stub(testbed):
    testbed.init_search_stub()


@pytest.fixture
def index(search_stub):
    return search.Index('products')


@pytest.fixture
def document():
    return search.Document(
        doc_id='doc1',
        fields=[
            search.TextField(name='title', value='Meep: A biography')])


def test_simple_search(index):
    snippets.simple_search(index)


def test_search_date(index):
    snippets.search_date(index)


def test_search_terms(index):
    snippets.search_terms(index)


def test_create_document():
    assert snippets.create_document()


def test_add_document_to_index(index, document):
    snippets.add_document_to_index(document)
    assert index.get(document.doc_id)


def test_add_document_and_get_doc_id(index, document):
    ids = snippets.add_document_and_get_doc_id([document])
    assert ids == [document.doc_id]


def test_get_document_by_id(index):
    index.put(search.Document(doc_id='AZ124'))
    index.put(search.Document(doc_id='AZ125'))
    index.put(search.Document(doc_id='AZ126'))

    doc, docs = snippets.get_document_by_id()

    assert doc.doc_id == 'AZ125'
    assert [x.doc_id for x in docs] == ['AZ125', 'AZ126']


def test_query_index(index):
    snippets.query_index()


def test_delete_all_in_index(index, document):
    index.put(document)
    snippets.delete_all_in_index(index)
    assert not index.get(document.doc_id)


def test_async_query(index):
    snippets.async_query(index)


def test_query_options(index):
    snippets.query_options()


def test_query_results(index, document):
    index.put(document)
    total_matches, list_of_docs, number_of_docs_returned = (
        snippets.query_results(index, 'meep'))

    assert total_matches == 1
    assert list_of_docs
    assert number_of_docs_returned == 1


def test_query_offset(index, document):
    index.put(document)
    snippets.query_offset(index, 'meep')


def test_query_cursor(index, document):
    index.put(document)
    snippets.query_cursor(index, 'meep')


def test_query_per_document_cursor(index, document):
    index.put(document)
    snippets.query_per_document_cursor(index, 'meep')


def test_saving_and_restoring_cursor(index):
    snippets.saving_and_restoring_cursor(search.Cursor())


def test_add_faceted_document(index):
    snippets.add_faceted_document(index)


def test_facet_discovery(index):
    snippets.add_faceted_document(index)
    snippets.facet_discovery(index)


def test_facet_by_name(index):
    snippets.add_faceted_document(index)
    snippets.facet_by_name(index)


def test_facet_by_name_and_value(index):
    snippets.add_faceted_document(index)
    snippets.facet_by_name_and_value(index)

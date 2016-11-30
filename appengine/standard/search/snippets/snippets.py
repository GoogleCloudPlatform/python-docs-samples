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

from datetime import datetime

from google.appengine.api import search


def simple_search(index):
    index.search('rose water')


def search_date(index):
    index.search('1776-07-04')


def search_terms(index):
    # search for documents with pianos that cost less than $5000
    index.search("product = piano AND price < 5000")


def create_document():
    document = search.Document(
        # Setting the doc_id is optional. If omitted, the search service will
        # create an identifier.
        doc_id='PA6-5000',
        fields=[
            search.TextField(name='customer', value='Joe Jackson'),
            search.HtmlField(
                name='comment', value='this is <em>marked up</em> text'),
            search.NumberField(name='number_of_visits', value=7),
            search.DateField(name='last_visit', value=datetime.now()),
            search.DateField(
                name='birthday', value=datetime(year=1960, month=6, day=19)),
            search.GeoField(
                name='home_location', value=search.GeoPoint(37.619, -122.37))
        ])
    return document


def add_document_to_index(document):
    index = search.Index('products')
    index.put(document)


def add_document_and_get_doc_id(documents):
    index = search.Index('products')
    results = index.put(documents)
    document_ids = [document.id for document in results]
    return document_ids


def get_document_by_id():
    index = search.Index('products')

    # Get a single document by ID.
    document = index.get("AZ125")

    # Get a range of documents starting with a given ID.
    documents = index.get_range(start_id="AZ125", limit=100)

    return document, documents


def query_index():
    index = search.Index('products')
    query_string = 'product: piano AND price < 5000'

    results = index.search(query_string)

    for scored_document in results:
        print(scored_document)


def delete_all_in_index(index):
    # index.get_range by returns up to 100 documents at a time, so we must
    # loop until we've deleted all items.
    while True:
        # Use ids_only to get the list of document IDs in the index without
        # the overhead of getting the entire document.
        document_ids = [
            document.doc_id
            for document
            in index.get_range(ids_only=True)]

        # If no IDs were returned, we've deleted everything.
        if not document_ids:
            break

        # Delete the documents for the given IDs
        index.delete(document_ids)


def async_query(index):
    futures = [index.search_async('foo'), index.search_async('bar')]
    results = [future.get_result() for future in futures]
    return results


def query_options():
    index = search.Index('products')
    query_string = "product: piano AND price < 5000"

    # Create sort options to sort on price and brand.
    sort_price = search.SortExpression(
        expression='price',
        direction=search.SortExpression.DESCENDING,
        default_value=0)
    sort_brand = search.SortExpression(
        expression='brand',
        direction=search.SortExpression.DESCENDING,
        default_value="")
    sort_options = search.SortOptions(expressions=[sort_price, sort_brand])

    # Create field expressions to add new fields to the scored documents.
    price_per_note_expression = search.FieldExpression(
        name='price_per_note', expression='price/88')
    ivory_expression = search.FieldExpression(
        name='ivory', expression='snippet("ivory", summary, 120)')

    # Create query options using the sort options and expressions created
    # above.
    query_options = search.QueryOptions(
        limit=25,
        returned_fields=['model', 'price', 'description'],
        returned_expressions=[price_per_note_expression, ivory_expression],
        sort_options=sort_options)

    # Build the Query and run the search
    query = search.Query(query_string=query_string, options=query_options)
    results = index.search(query)
    for scored_document in results:
        print(scored_document)


def query_results(index, query_string):
    result = index.search(query_string)
    total_matches = result.number_found
    list_of_docs = result.results
    number_of_docs_returned = len(list_of_docs)
    return total_matches, list_of_docs, number_of_docs_returned


def query_offset(index, query_string):
    offset = 0

    while True:
        # Build the query using the current offset.
        options = search.QueryOptions(offset=offset)
        query = search.Query(query_string=query_string, options=options)

        # Get the results
        results = index.search(query)

        number_retrieved = len(results.results)
        if number_retrieved == 0:
            break

        # Add the number of documents found to the offset, so that the next
        # iteration will grab the next page of documents.
        offset += number_retrieved

        # Process the matched documents
        for document in results:
            print(document)


def query_cursor(index, query_string):
    cursor = search.Cursor()

    while cursor:
        # Build the query using the cursor.
        options = search.QueryOptions(cursor=cursor)
        query = search.Query(query_string=query_string, options=options)

        # Get the results and the next cursor
        results = index.search(query)
        cursor = results.cursor

        for document in results:
            print(document)


def query_per_document_cursor(index, query_string):
    cursor = search.Cursor(per_result=True)

    # Build the query using the cursor.
    options = search.QueryOptions(cursor=cursor)
    query = search.Query(query_string=query_string, options=options)

    # Get the results.
    results = index.search(query)

    document_cursor = None
    for document in results:
        # discover some document of interest and grab its cursor, for this
        # sample we'll just use the first document.
        document_cursor = document.cursor
        break

    # Start the next search from the document of interest.
    if document_cursor is None:
        return

    options = search.QueryOptions(cursor=document_cursor)
    query = search.Query(query_string=query_string, options=options)
    results = index.search(query)

    for document in results:
        print(document)


def saving_and_restoring_cursor(cursor):
    # Convert the cursor to a web-safe string.
    cursor_string = cursor.web_safe_string
    # Restore the cursor from a web-safe string.
    cursor = search.Cursor(web_safe_string=cursor_string)


def add_faceted_document(index):
    document = search.Document(
        doc_id='doc1',
        fields=[
            search.AtomField(name='name', value='x86')],
        facets=[
            search.AtomFacet(name='type', value='computer'),
            search.NumberFacet(name='ram_size_gb', value=8)])

    index.put(document)


def facet_discovery(index):
    # Create the query and enable facet discovery.
    query = search.Query('name:x86', enable_facet_discovery=True)
    results = index.search(query)

    for facet in results.facets:
        print('facet {}.'.format(facet.name))
        for value in facet.values:
            print('{}: count={}, refinement_token={}'.format(
                value.label, value.count, value.refinement_token))


def facet_by_name(index):
    # Create the query and specify to only return the "type" and "ram_size_gb"
    # facets.
    query = search.Query('name:x86', return_facets=['type', 'ram_size_gb'])
    results = index.search(query)

    for facet in results.facets:
        print('facet {}'.format(facet.name))
        for value in facet.values:
            print('{}: count={}, refinement_token={}'.format(
                value.label, value.count, value.refinement_token))


def facet_by_name_and_value(index):
    # Create the query and specify to return the "type" facet with values
    # "computer" and "printer" and the "ram_size_gb" facet with value in the
    # ranges [0,4), [4, 8), and [8, max].
    query = search.Query(
        'name:x86',
        return_facets=[
            search.FacetRequest('type', values=['computer', 'printer']),
            search.FacetRequest('ram_size_gb', ranges=[
                search.FacetRange(end=4),
                search.FacetRange(start=4, end=8),
                search.FacetRange(start=8)])
        ])

    results = index.search(query)
    for facet in results.facets:
        print('facet {}'.format(facet.name))
        for value in facet.values:
            print('{}: count={}, refinement_token={}'.format(
                value.label, value.count, value.refinement_token))

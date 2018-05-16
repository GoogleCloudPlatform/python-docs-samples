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

import datetime

from google.cloud import firestore
import google.cloud.exceptions


def quickstart_new_instance():
    # [START fs_initialize]
    from google.cloud import firestore

    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()
    # [END fs_initialize]

    return db


def quickstart_add_data_one():
    db = firestore.Client()
    # [START fs_add_data_1]
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    # [END fs_add_data_1]


def quickstart_add_data_two():
    db = firestore.Client()
    # [START fs_add_data_2]
    doc_ref = db.collection(u'users').document(u'aturing')
    doc_ref.set({
        u'first': u'Alan',
        u'middle': u'Mathison',
        u'last': u'Turing',
        u'born': 1912
    })
    # [END fs_add_data_2]


def quickstart_get_collection():
    db = firestore.Client()
    # [START fs_get_all]
    users_ref = db.collection(u'users')
    docs = users_ref.get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # [END fs_get_all]


def add_from_dict():
    db = firestore.Client()
    # [START fs_set_document]
    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'cities').document(u'LA').set(data)
    # [END fs_set_document]


def add_data_types():
    db = firestore.Client()
    # [START fs_set_document_data_types]
    data = {
        u'stringExample': u'Hello, World!',
        u'booleanExample': True,
        u'numberExample': 3.14159265,
        u'dateExample': datetime.datetime.now(),
        u'arrayExample': [5, True, u'hello'],
        u'nullExample': None,
        u'objectExample': {
            u'a': 5,
            u'b': True
        }
    }

    db.collection(u'data').document(u'one').set(data)
    # [END fs_set_document_data_types]


# [START fs_class_definition]
class City(object):
    def __init__(self, name, state, country, capital=False, population=0):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        city = City(source[u'name'], source[u'state'], source[u'country'])

        if u'capital' in source:
            city.capital = source[u'capital']

        if u'population' in source:
            city.population = source[u'population']

        return city
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'name': self.name,
            u'state': self.state,
            u'country': self.country
        }

        if self.capital:
            dest[u'capital'] = self.capital

        if self.population:
            dest[u'population'] = self.population

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return u'City(name={}, country={}, population={}, capital={})'.format(
            self.name, self.country, self.population, self.capital)
# [END fs_class_definition]


def add_example_data():
    db = firestore.Client()
    # [START fs_retrieve_create_examples]
    # [START fs_query_create_examples]
    cities_ref = db.collection(u'cities')
    cities_ref.document(u'SF').set(
        City(u'San Francisco', u'CA', u'USA', False, 860000).to_dict())
    cities_ref.document(u'LA').set(
        City(u'Los Angeles', u'CA', u'USA', False, 3900000).to_dict())
    cities_ref.document(u'DC').set(
        City(u'Washington D.C.', None, u'USA', True, 680000).to_dict())
    cities_ref.document(u'TOK').set(
        City(u'Tokyo', None, u'Japan', True, 9000000).to_dict())
    cities_ref.document(u'BJ').set(
        City(u'Beijing', None, u'China', True, 21500000).to_dict())
    # [END fs_query_create_examples]
    # [END fs_retrieve_create_examples]


def add_custom_class_with_id():
    db = firestore.Client()
    # [START fs_set_document_custom_class]
    city = City(name=u'Los Angeles', state=u'CA', country=u'USA')
    db.collection(u'cities').document(u'LA').set(city.to_dict())
    # [END fs_set_document_custom_class]


def add_data_with_id():
    db = firestore.Client()
    data = {}
    # [START fs_set_requires_id]
    db.collection(u'cities').document(u'new-city-id').set(data)
    # [END fs_set_requires_id]


def add_custom_class_generated_id():
    db = firestore.Client()
    # [START fs_add_doc_data_with_auto_id]
    city = City(name=u'Tokyo', state=None, country=u'Japan')
    db.collection(u'cities').add(city.to_dict())
    # [END fs_add_doc_data_with_auto_id]


def add_new_doc():
    db = firestore.Client()
    # [START fs_add_doc_data_after_auto_id]
    new_city_ref = db.collection(u'cities').document()

    # later...
    new_city_ref.set({
        # ...
    })
    # [END fs_add_doc_data_after_auto_id]


def get_check_exists():
    db = firestore.Client()
    # [START fs_get_document]
    doc_ref = db.collection(u'cities').document(u'SF')

    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    # [END fs_get_document]


def get_custom_class():
    db = firestore.Client()
    # [START fs_get_document_custom_class]
    doc_ref = db.collection(u'cities').document(u'BJ')

    doc = doc_ref.get()
    city = City.from_dict(doc.to_dict())
    print(city)
    # [END fs_get_document_custom_class]


def get_simple_query():
    db = firestore.Client()
    # [START fs_get_multiple_docs]
    docs = db.collection(u'cities').where(u'capital', u'==', True).get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # [END fs_get_multiple_docs]


def get_full_collection():
    db = firestore.Client()
    # [START fs_get_all_docs]
    docs = db.collection(u'cities').get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # [END fs_get_all_docs]


def structure_doc_ref():
    db = firestore.Client()
    # [START fs_document_ref]
    a_lovelace_ref = db.collection(u'users').document(u'alovelace')
    # [END fs_document_ref]
    print(a_lovelace_ref)


def structure_collection_ref():
    db = firestore.Client()
    # [START fs_collection_ref]
    users_ref = db.collection(u'users')
    # [END fs_collection_ref]
    print(users_ref)


def structure_doc_ref_alternate():
    db = firestore.Client()
    # [START fs_document_path_ref]
    a_lovelace_ref = db.document(u'users/alovelace')
    # [END fs_document_path_ref]

    return a_lovelace_ref


def structure_subcollection_ref():
    db = firestore.Client()
    # [START fs_subcollection_ref]
    room_a_ref = db.collection(u'rooms').document(u'roomA')
    message_ref = room_a_ref.collection(u'messages').document(u'message1')
    # [END fs_subcollection_ref]
    print(message_ref)


def update_doc():
    db = firestore.Client()
    # [START fs_update_doc]
    city_ref = db.collection(u'cities').document(u'DC')

    # Set the capital field
    city_ref.update({u'capital': True})
    # [END fs_update_doc]


def update_multiple():
    db = firestore.Client()
    # [START fs_update_multiple]
    doc_ref = db.collection(u'cities').document(u'DC')

    doc_ref.update({
        u'name': u'Washington D.C.',
        u'country': u'USA',
        u'capital': True
    })
    # [END fs_update_multiple]


def update_create_if_missing():
    db = firestore.Client()
    # [START fs_update_create_if_missing]
    city_ref = db.collection(u'cities').document(u'BJ')

    city_ref.update({
        u'capital': True
    }, firestore.CreateIfMissingOption(True))
    # [END fs_update_create_if_missing]


def update_nested():
    db = firestore.Client()
    # [START fs_update_nested_fields]
    # Create an initial document to update
    frank_ref = db.collection(u'users').document(u'frank')
    frank_ref.set({
        u'name': u'Frank',
        u'favorites': {
            u'food': u'Pizza',
            u'color': u'Blue',
            u'subject': u'Recess'
        },
        u'age': 12
    })

    # Update age and favorite color
    frank_ref.update({
        u'age': 13,
        u'favorites.color': u'Red'
    })
    # [END fs_update_nested_fields]


def update_server_timestamp():
    db = firestore.Client()
    # [START fs_update_server_timestamp]
    city_ref = db.collection(u'objects').document(u'some-id')
    city_ref.update({
        u'timestamp': firestore.SERVER_TIMESTAMP
    })
    # [END fs_update_server_timestamp]


def update_data_transaction():
    db = firestore.Client()
    # [START fs_run_simple_transaction]
    transaction = db.transaction()
    city_ref = db.collection(u'cities').document(u'SF')

    @firestore.transactional
    def update_in_transaction(transaction, city_ref):
        snapshot = city_ref.get(transaction=transaction)
        transaction.update(city_ref, {
            u'population': snapshot.get(u'population') + 1
        })

    update_in_transaction(transaction, city_ref)
    # [END fs_run_simple_transaction]


def update_data_transaction_result():
    db = firestore.Client()
    # [START fs_return_info_transaction]
    transaction = db.transaction()
    city_ref = db.collection(u'cities').document(u'SF')

    @firestore.transactional
    def update_in_transaction(transaction, city_ref):
        snapshot = city_ref.get(transaction=transaction)
        new_population = snapshot.get(u'population') + 1

        if new_population < 1000000:
            transaction.update(city_ref, {
                u'population': new_population
            })
            return True
        else:
            return False

    result = update_in_transaction(transaction, city_ref)
    if result:
        print(u'Population updated')
    else:
        print(u'Sorry! Population is too big.')
    # [END fs_return_info_transaction]


def update_data_batch():
    db = firestore.Client()
    # [START fs_batch_write]
    batch = db.batch()

    # Set the data for NYC
    nyc_ref = db.collection(u'cities').document(u'NYC')
    batch.set(nyc_ref, {u'name': u'New York City'})

    # Update the population for SF
    sf_ref = db.collection(u'cities').document(u'SF')
    batch.update(sf_ref, {u'population': 1000000})

    # Delete LA
    la_ref = db.collection(u'cities').document(u'LA')
    batch.delete(la_ref)

    # Commit the batch
    batch.commit()
    # [END fs_batch_write]


def compound_query_example():
    db = firestore.Client()
    # [START fs_create_query_state]
    # Create a reference to the cities collection
    cities_ref = db.collection(u'cities')

    # Create a query against the collection
    query_ref = cities_ref.where(u'state', u'==', u'CA')
    # [END fs_create_query_state]

    return query_ref


def compound_query_simple():
    db = firestore.Client()
    # [START fs_create_query_capital]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(u'capital', u'==', True)
    # [END fs_create_query_capital]

    print(query)


def compound_query_single_clause():
    db = firestore.Client()
    # [START fs_simple_queries]
    cities_ref = db.collection(u'cities')

    cities_ref.where(u'state', u'==', u'CA')
    cities_ref.where(u'population', u'<', 1000000)
    cities_ref.where(u'name', u'>=', u'San Francisco')
    # [END fs_simple_queries]


def compound_query_valid_multi_clause():
    db = firestore.Client()
    cities_ref = db.collection(u'cities')

    # [START fs_chained_query]
    sydney_query = cities_ref.where(
        u'state', u'==', u'CO').where(u'name', u'==', u'Denver')
    # [END fs_chained_query]
    # [START fs_composite_index_chained_query]
    large_us_cities_query = cities_ref.where(
        u'state', u'==', u'CA').where(u'population', u'>', 1000000)
    # [END fs_composite_index_chained_query]
    print(sydney_query)
    print(large_us_cities_query)


def compound_query_valid_single_field():
    db = firestore.Client()
    # [START fs_range_query]
    cities_ref = db.collection(u'cities')
    cities_ref.where(u'state', u'>=', u'CA').where(u'state', u'<=', u'IN')
    # [END fs_range_query]


def compound_query_invalid_multi_field():
    db = firestore.Client()
    # [START fs_invalid_range_query]
    cities_ref = db.collection(u'cities')
    cities_ref.where(
        u'state', u'>=', u'CA').where(u'population', u'>=', 1000000)
    # [END fs_invalid_range_query]


def order_simple_limit():
    db = firestore.Client()
    # [START fs_order_by_name_limit_query]
    db.collection(u'cities').order_by(u'name').limit(3).get()
    # [END fs_order_by_name_limit_query]


def order_simple_limit_desc():
    db = firestore.Client()
    # [START fs_order_by_name_desc_limit_query]
    cities_ref = db.collection(u'cities')
    query = cities_ref.order_by(
        u'name', direction=firestore.Query.DESCENDING).limit(3)
    results = query.get()
    # [END fs_order_by_name_desc_limit_query]
    print(results)


def order_multiple():
    db = firestore.Client()
    # [START fs_order_by_state_and_population_query]
    cities_ref = db.collection(u'cities')
    cities_ref.order_by(u'state').order_by(
        u'population', direction=firestore.Query.DESCENDING)
    # [END fs_order_by_state_and_population_query]


def order_where_limit():
    db = firestore.Client()
    # [START fs_where_order_by_limit_query]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(
        u'population', u'>', 2500000).order_by(u'population').limit(2)
    results = query.get()
    # [END fs_where_order_by_limit_query]
    print(results)


def order_where_valid():
    db = firestore.Client()
    # [START fs_range_order_by_query]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(
        u'population', u'>', 2500000).order_by(u'population')
    results = query.get()
    # [END fs_range_order_by_query]
    print(results)


def order_where_invalid():
    db = firestore.Client()
    # [START fs_invalid_range_order_by_query]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(u'population', u'>', 2500000).order_by(u'country')
    results = query.get()
    # [END fs_invalid_range_order_by_query]
    print(results)


def cursor_simple_start_at():
    db = firestore.Client()
    # [START fs_start_at_field_query_cursor]
    cities_ref = db.collection(u'cities')
    query_start_at = cities_ref.order_by(u'population').start_at({
        u'population': 1000000
    })
    # [END fs_start_at_field_query_cursor]

    return query_start_at


def cursor_simple_end_at():
    db = firestore.Client()
    # [START fs_end_at_field_query_cursor]
    cities_ref = db.collection(u'cities')
    query_end_at = cities_ref.order_by(u'population').end_at({
        u'population': 1000000
    })
    # [END fs_end_at_field_query_cursor]

    return query_end_at


def cursor_paginate():
    db = firestore.Client()
    # [START fs_paginated_query_cursor]
    cities_ref = db.collection(u'cities')
    first_query = cities_ref.order_by(u'population').limit(3)

    # Get the last document from the results
    docs = first_query.get()
    last_doc = list(docs)[-1]

    # Construct a new query starting at this document
    # Note: this will not have the desired effect if
    # multiple cities have the exact same population value
    last_pop = last_doc.to_dict()[u'population']

    next_query = (
        cities_ref
        .order_by(u'population')
        .start_after({
            u'population': last_pop
        })
        .limit(3)
    )
    # Use the query for pagination
    # ...
    # [END fs_paginated_query_cursor]

    return next_query


def cursor_multiple_conditions():
    db = firestore.Client()
    # [START fs_multiple_cursor_conditions]
    start_at_name = (
        db.collection(u'cities')
        .order_by(u'name')
        .order_by(u'state')
        .start_at({
            u'name': u'Springfield'
        })
    )

    start_at_name_and_state = (
        db.collection(u'cities')
        .order_by(u'name')
        .order_by(u'state')
        .start_at({
            u'name': u'Springfield',
            u'state': u'Missouri'
        })
    )
    # [END fs_multiple_cursor_conditions]

    return start_at_name, start_at_name_and_state


def delete_single_doc():
    db = firestore.Client()
    # [START fs_delete_doc]
    db.collection(u'cities').document(u'DC').delete()
    # [END fs_delete_doc]


def delete_field():
    db = firestore.Client()
    # [START fs_delete_field]
    city_ref = db.collection(u'cities').document(u'BJ')
    city_ref.update({
        u'capital': firestore.DELETE_FIELD
    })
    # [END fs_delete_field]


def delete_full_collection():
    db = firestore.Client()

    # [START fs_delete_collection]
    def delete_collection(coll_ref, batch_size):
        docs = coll_ref.limit(10).get()
        deleted = 0

        for doc in docs:
            print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
            doc.reference.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)
    # [END fs_delete_collection]

    delete_collection(db.collection(u'cities'), 10)

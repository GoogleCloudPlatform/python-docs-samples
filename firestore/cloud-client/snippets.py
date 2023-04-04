# Copyright 2017 Google, LLC.
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

import datetime
import threading
from time import sleep

from google.api_core.client_options import ClientOptions
from google.cloud import firestore


def quickstart_new_instance():
    # [START firestore_setup_client_create]
    # [START firestore_setup_client_create_with_project_id]
    from google.cloud import firestore

    # The `project` parameter is optional and represents which project the client
    # will act on behalf of. If not supplied, the client falls back to the default
    # project inferred from the environment.
    db = firestore.Client(project='my-project-id')
    # [END firestore_setup_client_create_with_project_id]
    # [END firestore_setup_client_create]

    return db


def quickstart_add_data_one():
    db = firestore.Client()
    # [START firestore_setup_dataset_pt1]
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    # [END firestore_setup_dataset_pt1]


def quickstart_add_data_two():
    db = firestore.Client()
    # [START firestore_setup_dataset_pt2]
    doc_ref = db.collection(u'users').document(u'aturing')
    doc_ref.set({
        u'first': u'Alan',
        u'middle': u'Mathison',
        u'last': u'Turing',
        u'born': 1912
    })
    # [END firestore_setup_dataset_pt2]


def quickstart_get_collection():
    db = firestore.Client()
    # [START firestore_setup_dataset_read]
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    # [END firestore_setup_dataset_read]


def add_from_dict():
    db = firestore.Client()
    # [START firestore_data_set_from_map]
    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'cities').document(u'LA').set(data)
    # [END firestore_data_set_from_map]


def add_data_types():
    db = firestore.Client()
    # [START firestore_data_set_from_map_nested]
    data = {
        u'stringExample': u'Hello, World!',
        u'booleanExample': True,
        u'numberExample': 3.14159265,
        u'dateExample': datetime.datetime.now(tz=datetime.timezone.utc),
        u'arrayExample': [5, True, u'hello'],
        u'nullExample': None,
        u'objectExample': {
            u'a': 5,
            u'b': True
        }
    }

    db.collection(u'data').document(u'one').set(data)
    # [END firestore_data_set_from_map_nested]


# [START firestore_data_custom_type_definition]
class City(object):
    def __init__(self, name, state, country, capital=False, population=0,
                 regions=[]):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population
        self.regions = regions

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        city = City(source[u'name'], source[u'state'], source[u'country'])

        if u'capital' in source:
            city.capital = source[u'capital']

        if u'population' in source:
            city.population = source[u'population']

        if u'regions' in source:
            city.regions = source[u'regions']

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

        if self.regions:
            dest[u'regions'] = self.regions

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return (
            f'City(\
                name={self.name}, \
                country={self.country}, \
                population={self.population}, \
                capital={self.capital}, \
                regions={self.regions}\
            )'
        )
# [END firestore_data_custom_type_definition]


def add_example_data():
    db = firestore.Client()
    # [START firestore_data_get_dataset]
    cities_ref = db.collection(u'cities')
    cities_ref.document(u'BJ').set(
        City(u'Beijing', None, u'China', True, 21500000, [u'hebei']).to_dict())
    cities_ref.document(u'SF').set(
        City(u'San Francisco', u'CA', u'USA', False, 860000,
             [u'west_coast', u'norcal']).to_dict())
    cities_ref.document(u'LA').set(
        City(u'Los Angeles', u'CA', u'USA', False, 3900000,
             [u'west_coast', u'socal']).to_dict())
    cities_ref.document(u'DC').set(
        City(u'Washington D.C.', None, u'USA', True, 680000,
             [u'east_coast']).to_dict())
    cities_ref.document(u'TOK').set(
        City(u'Tokyo', None, u'Japan', True, 9000000,
             [u'kanto', u'honshu']).to_dict())
    # [END firestore_data_get_dataset]


def add_custom_class_with_id():
    db = firestore.Client()
    # [START firestore_data_set_from_custom_type]
    city = City(name=u'Los Angeles', state=u'CA', country=u'USA')
    db.collection(u'cities').document(u'LA').set(city.to_dict())
    # [END firestore_data_set_from_custom_type]


def add_data_with_id():
    db = firestore.Client()
    data = {}
    # [START firestore_data_set_id_specified]
    db.collection(u'cities').document(u'new-city-id').set(data)
    # [END firestore_data_set_id_specified]


def add_custom_class_generated_id():
    db = firestore.Client()
    # [START firestore_data_set_id_random_collection]
    city = {
        u'name': u'Tokyo',
        u'country': u'Japan'
    }
    update_time, city_ref = db.collection(u'cities').add(city)
    print(f'Added document with id {city_ref.id}')
    # [END firestore_data_set_id_random_collection]


def add_new_doc():
    db = firestore.Client()
    # [START firestore_data_set_id_random_document_ref]
    new_city_ref = db.collection(u'cities').document()

    # later...
    new_city_ref.set({
        # ...
    })
    # [END firestore_data_set_id_random_document_ref]


def get_check_exists():
    db = firestore.Client()
    # [START firestore_data_get_as_map]
    doc_ref = db.collection(u'cities').document(u'SF')

    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')
    # [END firestore_data_get_as_map]


def get_custom_class():
    db = firestore.Client()
    # [START firestore_data_get_as_custom_type]
    doc_ref = db.collection(u'cities').document(u'BJ')

    doc = doc_ref.get()
    city = City.from_dict(doc.to_dict())
    print(city)
    # [END firestore_data_get_as_custom_type]


def get_simple_query():
    db = firestore.Client()
    # [START firestore_data_query]
    # Note: Use of CollectionRef stream() is prefered to get()
    docs = db.collection(u'cities').where(u'capital', u'==', True).stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    # [END firestore_data_query]


def array_contains_filter():
    db = firestore.Client()
    # [START firestore_query_filter_array_contains]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(u'regions', u'array_contains', u'west_coast')
    # [END firestore_query_filter_array_contains]
    docs = query.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')


def get_full_collection():
    db = firestore.Client()
    # [START firestore_data_get_all_documents]
    docs = db.collection(u'cities').stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    # [END firestore_data_get_all_documents]


def structure_doc_ref():
    db = firestore.Client()
    # [START firestore_data_reference_document]
    a_lovelace_ref = db.collection(u'users').document(u'alovelace')
    # [END firestore_data_reference_document]
    print(a_lovelace_ref)


def structure_collection_ref():
    db = firestore.Client()
    # [START firestore_data_reference_collection]
    users_ref = db.collection(u'users')
    # [END firestore_data_reference_collection]
    print(users_ref)


def structure_doc_ref_alternate():
    db = firestore.Client()
    # [START firestore_data_reference_document_path]
    a_lovelace_ref = db.document(u'users/alovelace')
    # [END firestore_data_reference_document_path]

    return a_lovelace_ref


def structure_subcollection_ref():
    db = firestore.Client()
    # [START firestore_data_reference_subcollection]
    room_a_ref = db.collection(u'rooms').document(u'roomA')
    message_ref = room_a_ref.collection(u'messages').document(u'message1')
    # [END firestore_data_reference_subcollection]
    print(message_ref)


def update_doc():
    db = firestore.Client()
    db.collection(u'cities').document(u'DC').set(
        City(u'Washington D.C.', None, u'USA', True, 680000,
             [u'east_coast']).to_dict())

    # [START firestore_data_set_field]
    city_ref = db.collection(u'cities').document(u'DC')

    # Set the capital field
    city_ref.update({u'capital': True})
    # [END firestore_data_set_field]


def update_doc_array():
    db = firestore.Client()
    db.collection(u'cities').document(u'DC').set(
        City(u'Washington D.C.', None, u'USA', True, 680000,
             [u'east_coast']).to_dict())

    # [START firestore_data_set_array_operations]
    city_ref = db.collection(u'cities').document(u'DC')

    # Atomically add a new region to the 'regions' array field.
    city_ref.update({u'regions': firestore.ArrayUnion([u'greater_virginia'])})

    # // Atomically remove a region from the 'regions' array field.
    city_ref.update({u'regions': firestore.ArrayRemove([u'east_coast'])})
    # [END firestore_data_set_array_operations]
    city = city_ref.get()
    print(f'Updated the regions field of the DC. {city.to_dict()}')


def update_multiple():
    db = firestore.Client()
    db.collection(u'cities').document(u'DC').set(
        City(u'Washington D.C.', None, u'USA', True, 680000,
             [u'east_coast']).to_dict())

    # [START firestore_update_multiple]
    doc_ref = db.collection(u'cities').document(u'DC')

    doc_ref.update({
        u'name': u'Washington D.C.',
        u'country': u'USA',
        u'capital': True
    })
    # [END firestore_update_multiple]


def update_create_if_missing():
    db = firestore.Client()
    # [START firestore_data_set_doc_upsert]
    city_ref = db.collection(u'cities').document(u'BJ')

    city_ref.set({
        u'capital': True
    }, merge=True)
    # [END firestore_data_set_doc_upsert]


def update_nested():
    db = firestore.Client()
    # [START firestore_data_set_nested_fields]
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
    # [END firestore_data_set_nested_fields]


def update_server_timestamp():
    db = firestore.Client()
    # [START firestore_data_set_server_timestamp]
    city_ref = db.collection(u'objects').document(u'some-id')
    city_ref.update({
        u'timestamp': firestore.SERVER_TIMESTAMP
    })
    # [END firestore_data_set_server_timestamp]


def update_data_transaction():
    db = firestore.Client()
    # [START firestore_transaction_document_update]
    transaction = db.transaction()
    city_ref = db.collection(u'cities').document(u'SF')

    @firestore.transactional
    def update_in_transaction(transaction, city_ref):
        snapshot = city_ref.get(transaction=transaction)
        transaction.update(city_ref, {
            u'population': snapshot.get(u'population') + 1
        })

    update_in_transaction(transaction, city_ref)
    # [END firestore_transaction_document_update]


def update_data_transaction_result():
    db = firestore.Client()
    # [START firestore_transaction_document_update_conditional]
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
    # [END firestore_transaction_document_update_conditional]


def update_data_batch():
    db = firestore.Client()
    # [START firestore_data_batch_writes]
    batch = db.batch()

    # Set the data for NYC
    nyc_ref = db.collection(u'cities').document(u'NYC')
    batch.set(nyc_ref, {u'name': u'New York City'})

    # Update the population for SF
    sf_ref = db.collection(u'cities').document(u'SF')
    batch.update(sf_ref, {u'population': 1000000})

    # Delete DEN
    den_ref = db.collection(u'cities').document(u'DEN')
    batch.delete(den_ref)

    # Commit the batch
    batch.commit()
    # [END firestore_data_batch_writes]


def compound_query_example():
    db = firestore.Client()
    # [START firestore_query_filter_eq_string]
    # Create a reference to the cities collection
    cities_ref = db.collection(u'cities')

    # Create a query against the collection
    query_ref = cities_ref.where(u'state', u'==', u'CA')
    # [END firestore_query_filter_eq_string]

    return query_ref


def compound_query_simple():
    db = firestore.Client()
    # [START firestore_query_filter_eq_boolean]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(u'capital', u'==', True)
    # [END firestore_query_filter_eq_boolean]

    print(query)


def compound_query_single_clause():
    db = firestore.Client()
    # [START firestore_query_filter_single_examples]
    cities_ref = db.collection(u'cities')

    cities_ref.where(u'state', u'==', u'CA')
    cities_ref.where(u'population', u'<', 1000000)
    cities_ref.where(u'name', u'>=', u'San Francisco')
    # [END firestore_query_filter_single_examples]


def compound_query_valid_multi_clause():
    db = firestore.Client()
    # [START firestore_query_filter_compound_multi_eq]
    cities_ref = db.collection(u'cities')

    denver_query = cities_ref.where(
        u'state', u'==', u'CO').where(u'name', u'==', u'Denver')
    large_us_cities_query = cities_ref.where(
        u'state', u'==', u'CA').where(u'population', u'>', 1000000)
    # [END firestore_query_filter_compound_multi_eq]
    print(denver_query)
    print(large_us_cities_query)


def compound_query_valid_single_field():
    db = firestore.Client()
    # [START firestore_query_filter_range_valid]
    cities_ref = db.collection(u'cities')
    cities_ref.where(u'state', u'>=', u'CA').where(u'state', u'<=', u'IN')
    # [END firestore_query_filter_range_valid]


def compound_query_invalid_multi_field():
    db = firestore.Client()
    # [START firestore_query_filter_range_invalid]
    cities_ref = db.collection(u'cities')
    cities_ref.where(
        u'state', u'>=', u'CA').where(u'population', u'>=', 1000000)
    # [END firestore_query_filter_range_invalid]


def order_simple_limit():
    db = firestore.Client()
    # [START firestore_order_simple_limit]
    db.collection(u'cities').order_by(u'name').limit(3).stream()
    # [END firestore_order_simple_limit]


def order_simple_limit_desc():
    db = firestore.Client()
    # [START firestore_query_order_desc_limit]
    cities_ref = db.collection(u'cities')
    query = cities_ref.order_by(
        u'name', direction=firestore.Query.DESCENDING).limit(3)
    results = query.stream()
    # [END firestore_query_order_desc_limit]
    print(results)


def order_multiple():
    db = firestore.Client()
    # [START firestore_query_order_multi]
    cities_ref = db.collection(u'cities')
    cities_ref.order_by(u'state').order_by(
        u'population', direction=firestore.Query.DESCENDING)
    # [END firestore_query_order_multi]


def order_where_limit():
    db = firestore.Client()
    # [START firestore_query_order_limit_field_valid]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(
        u'population', u'>', 2500000).order_by(u'population').limit(2)
    results = query.stream()
    # [END firestore_query_order_limit_field_valid]
    print(results)


def order_limit_to_last():
    db = firestore.Client()
    # [START firestore_query_order_limit]
    cities_ref = db.collection("cities")
    query = cities_ref.order_by("name").limit_to_last(2)
    results = query.get()
    # [END firestore_query_order_limit]
    print(results)


def order_where_valid():
    db = firestore.Client()
    # [START firestore_query_order_with_filter]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(
        u'population', u'>', 2500000).order_by(u'population')
    results = query.stream()
    # [END firestore_query_order_with_filter]
    print(results)


def order_where_invalid():
    db = firestore.Client()
    # [START firestore_query_order_field_invalid]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(u'population', u'>', 2500000).order_by(u'country')
    results = query.stream()
    # [END firestore_query_order_field_invalid]
    print(results)


def cursor_simple_start_at():
    db = firestore.Client()
    # [START firestore_query_cursor_start_at_field_value_single]
    cities_ref = db.collection(u'cities')
    query_start_at = cities_ref.order_by(u'population').start_at({
        u'population': 1000000
    })
    # [END firestore_query_cursor_start_at_field_value_single]

    return query_start_at


def cursor_simple_end_at():
    db = firestore.Client()
    # [START firestore_query_cursor_end_at_field_value_single]
    cities_ref = db.collection(u'cities')
    query_end_at = cities_ref.order_by(u'population').end_at({
        u'population': 1000000
    })
    # [END firestore_query_cursor_end_at_field_value_single]

    return query_end_at


def snapshot_cursors():
    db = firestore.Client()
    # [START firestore_query_cursor_start_at_document]
    doc_ref = db.collection(u'cities').document(u'SF')

    snapshot = doc_ref.get()
    start_at_snapshot = db.collection(
        u'cities').order_by(u'population').start_at(snapshot)
    # [END firestore_query_cursor_start_at_document]
    results = start_at_snapshot.limit(10).stream()
    for doc in results:
        print(f'{doc.id}')

    return results


def cursor_paginate():
    db = firestore.Client()
    # [START firestore_query_cursor_pagination]
    cities_ref = db.collection(u'cities')
    first_query = cities_ref.order_by(u'population').limit(3)

    # Get the last document from the results
    docs = first_query.stream()
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
    # [END firestore_query_cursor_pagination]

    return next_query


def listen_document():
    db = firestore.Client()
    # [START firestore_listen_document]

    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')
        callback_done.set()

    doc_ref = db.collection(u'cities').document(u'SF')

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)
    # [END firestore_listen_document]

    # Creating document
    data = {
        u'name': u'San Francisco',
        u'state': u'CA',
        u'country': u'USA',
        u'capital': False,
        u'population': 860000
    }
    doc_ref.set(data)
    # Wait for the callback.
    callback_done.wait(timeout=60)
    # [START firestore_listen_detach]
    # Terminate watch on a document
    doc_watch.unsubscribe()
    # [END firestore_listen_detach]


def listen_multiple():
    db = firestore.Client()
    # [START firestore_listen_query_snapshots]

    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        print(u'Callback received query snapshot.')
        print(u'Current cities in California:')
        for doc in col_snapshot:
            print(f'{doc.id}')
        callback_done.set()

    col_query = db.collection(u'cities').where(u'state', u'==', u'CA')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    # [END firestore_listen_query_snapshots]
    # Creating document
    data = {
        u'name': u'San Francisco',
        u'state': u'CA',
        u'country': u'USA',
        u'capital': False,
        u'population': 860000
    }
    db.collection(u'cities').document(u'SF').set(data)
    # Wait for the callback.
    callback_done.wait(timeout=60)
    query_watch.unsubscribe()


def listen_for_changes():
    db = firestore.Client()
    # [START firestore_listen_query_changes]

    # Create an Event for notifying main thread.
    delete_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        print(u'Callback received query snapshot.')
        print(u'Current cities in California: ')
        for change in changes:
            if change.type.name == 'ADDED':
                print(f'New city: {change.document.id}')
            elif change.type.name == 'MODIFIED':
                print(f'Modified city: {change.document.id}')
            elif change.type.name == 'REMOVED':
                print(f'Removed city: {change.document.id}')
                delete_done.set()

    col_query = db.collection(u'cities').where(u'state', u'==', u'CA')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    # [END firestore_listen_query_changes]
    mtv_document = db.collection(u'cities').document(u'MTV')
    # Creating document
    mtv_document.set({
        u'name': u'Mountain View',
        u'state': u'CA',
        u'country': u'USA',
        u'capital': False,
        u'population': 80000
    })
    sleep(1)

    # Modifying document
    mtv_document.update({
        u'name': u'Mountain View',
        u'state': u'CA',
        u'country': u'USA',
        u'capital': False,
        u'population': 90000
    })
    sleep(1)

    # Delete document
    mtv_document.delete()

    # Wait for the callback captures the deletion.
    delete_done.wait(timeout=60)
    query_watch.unsubscribe()


def cursor_multiple_conditions():
    db = firestore.Client()
    # [START firestore_query_cursor_start_at_field_value_multi]
    start_at_name = (
        db.collection(u'cities')
        .order_by(u'name')
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
    # [END firestore_query_cursor_start_at_field_value_multi]

    return start_at_name, start_at_name_and_state


def delete_single_doc():
    db = firestore.Client()
    # [START firestore_data_delete_doc]
    db.collection(u'cities').document(u'DC').delete()
    # [END firestore_data_delete_doc]


def delete_field():
    db = firestore.Client()
    # [START firestore_data_delete_field]
    city_ref = db.collection(u'cities').document(u'BJ')
    city_ref.update({
        u'capital': firestore.DELETE_FIELD
    })
    # [END firestore_data_delete_field]


def delete_full_collection():
    db = firestore.Client()

    # [START firestore_data_delete_collection]
    def delete_collection(coll_ref, batch_size):
        docs = coll_ref.list_documents(page_size=batch_size)
        deleted = 0

        for doc in docs:
            print(f'Deleting doc {doc.id} => {doc.get().to_dict()}')
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)
    # [END firestore_data_delete_collection]

    delete_collection(db.collection(u'cities'), 10)
    delete_collection(db.collection(u'data'), 10)
    delete_collection(db.collection(u'objects'), 10)
    delete_collection(db.collection(u'users'), 10)


def collection_group_query(db):
    # [START firestore_query_collection_group_dataset]
    cities = db.collection(u'cities')

    sf_landmarks = cities.document(u'SF').collection(u'landmarks')
    sf_landmarks.document().set({
        u'name': u'Golden Gate Bridge',
        u'type': u'bridge'
    })
    sf_landmarks.document().set({
        u'name': u'Legion of Honor',
        u'type': u'museum'
    })
    la_landmarks = cities.document(u'LA').collection(u'landmarks')
    la_landmarks.document().set({
        u'name': u'Griffith Park',
        u'type': u'park'
    })
    la_landmarks.document().set({
        u'name': u'The Getty',
        u'type': u'museum'
    })
    dc_landmarks = cities.document(u'DC').collection(u'landmarks')
    dc_landmarks.document().set({
        u'name': u'Lincoln Memorial',
        u'type': u'memorial'
    })
    dc_landmarks.document().set({
        u'name': u'National Air and Space Museum',
        u'type': u'museum'
    })
    tok_landmarks = cities.document(u'TOK').collection(u'landmarks')
    tok_landmarks.document().set({
        u'name': u'Ueno Park',
        u'type': u'park'
    })
    tok_landmarks.document().set({
        u'name': u'National Museum of Nature and Science',
        u'type': u'museum'
    })
    bj_landmarks = cities.document(u'BJ').collection(u'landmarks')
    bj_landmarks.document().set({
        u'name': u'Jingshan Park',
        u'type': u'park'
    })
    bj_landmarks.document().set({
        u'name': u'Beijing Ancient Observatory',
        u'type': u'museum'
    })
    # [END firestore_query_collection_group_dataset]

    # [START firestore_query_collection_group_filter_eq]
    museums = db.collection_group(u'landmarks')\
        .where(u'type', u'==', u'museum')
    docs = museums.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    # [END firestore_query_collection_group_filter_eq]
    return docs


def array_contains_any_queries(db):
    # [START firestore_query_filter_array_contains_any]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(
        u'regions', u'array_contains_any', [u'west_coast', u'east_coast']
    )
    return query
    # [END firestore_query_filter_array_contains_any]


def in_query_without_array(db):
    # [START firestore_query_filter_in]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(u'country', u'in', [u'USA', u'Japan'])
    return query
    # [END firestore_query_filter_in]


def in_query_with_array(db):
    # [START firestore_query_filter_in_with_array]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(
        u'regions', u'in', [[u'west_coast'], [u'east_coast']]
    )
    return query
    # [END firestore_query_filter_in_with_array]


def update_document_increment(db):
    # [START firestore_data_set_numeric_increment]
    washington_ref = db.collection(u'cities').document(u'DC')

    washington_ref.update({"population": firestore.Increment(50)})
    # [END firestore_data_set_numeric_increment]


def list_document_subcollections():
    db = firestore.Client()
    # [START firestore_data_get_sub_collections]
    collections = db.collection('cities').document('SF').collections()
    for collection in collections:
        for doc in collection.stream():
            print(f'{doc.id} => {doc.to_dict()}')
    # [END firestore_data_get_sub_collections]


def _setup_bundle():
    from google.cloud import firestore
    db = firestore.Client()
    db.collection("stories").document("news-item").set({"title": "Wow!"})


def create_and_build_bundle():
    _setup_bundle()
    # [START firestore_create_and_build_bundle]
    from google.cloud import firestore
    from google.cloud.firestore_bundle import FirestoreBundle

    db = firestore.Client()
    bundle = FirestoreBundle("latest-stories")

    doc_snapshot = db.collection("stories").document("news-item").get()
    query = db.collection("stories")._query()

    # Build the bundle
    # Note how `query` is named "latest-stories-query"
    bundle_buffer: str = bundle.add_document(doc_snapshot).add_named_query(
        "latest-stories-query", query,
    ).build()
    # [END firestore_create_and_build_bundle]

    return bundle, bundle_buffer


def regional_endpoint():
    # [START firestore_regional_endpoint]
    ENDPOINT = "nam5-firestore.googleapis.com"
    client_options = ClientOptions(api_endpoint=ENDPOINT)
    db = firestore.Client(client_options=client_options)

    count_query = db.collection(u'cities').limit(2).get()
    for r in count_query:
        print(r)
    # [END firestore_regional_endpoint]

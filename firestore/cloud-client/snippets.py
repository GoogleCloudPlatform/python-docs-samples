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
    # [START quickstart_new_instance]
    from google.cloud import firestore

    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()
    # [END quickstart_new_instance]

    return db


def quickstart_add_data_one():
    db = firestore.Client()
    # [START quickstart_add_data_one]
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    # [END quickstart_add_data_one]


def quickstart_add_data_two():
    db = firestore.Client()
    # [START quickstart_add_data_two]
    doc_ref = db.collection(u'users').document(u'aturing')
    doc_ref.set({
        u'first': u'Alan',
        u'middle': u'Mathison',
        u'last': u'Turing',
        u'born': 1912
    })
    # [END quickstart_add_data_two]


def quickstart_get_collection():
    db = firestore.Client()
    # [START quickstart_get_collection]
    users_ref = db.collection(u'users')
    docs = users_ref.get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # [END quickstart_get_collection]


def add_from_dict():
    db = firestore.Client()
    # [START add_from_dict]
    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'cities').document(u'LA').set(data)
    # [END add_from_dict]


def add_data_types():
    db = firestore.Client()
    # [START add_data_types]
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
    # [END add_data_types]


# [START custom_class_def]
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
# [END custom_class_def]


def add_example_data():
    db = firestore.Client()
    # [START add_example_data]
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
    # [END add_example_data]


def add_custom_class_with_id():
    db = firestore.Client()
    # [START add_custom_class_with_id]
    city = City(name=u'Los Angeles', state=u'CA', country=u'USA')
    db.collection(u'cities').document(u'LA').set(city.to_dict())
    # [END add_custom_class_with_id]


def add_data_with_id():
    db = firestore.Client()
    data = {}
    # [START add_data_with_id]
    db.collection(u'cities').document(u'new-city-id').set(data)
    # [END add_data_with_id]


def add_custom_class_generated_id():
    db = firestore.Client()
    # [START add_custom_class_generated_id]
    city = City(name=u'Tokyo', state=None, country=u'Japan')
    db.collection(u'cities').add(city.to_dict())
    # [END add_custom_class_generated_id]


def add_new_doc():
    db = firestore.Client()
    # [START add_new_doc]
    new_city_ref = db.collection(u'cities').document()

    # later...
    new_city_ref.set({
        # ...
    })
    # [END add_new_doc]


def get_check_exists():
    db = firestore.Client()
    # [START get_check_exists]
    doc_ref = db.collection(u'cities').document(u'SF')

    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    # [END get_check_exists]


def get_custom_class():
    db = firestore.Client()
    # [START get_custom_class]
    doc_ref = db.collection(u'cities').document(u'BJ')

    doc = doc_ref.get()
    city = City.from_dict(doc.to_dict())
    print(city)
    # [END get_custom_class]


def get_simple_query():
    db = firestore.Client()
    # [START get_simple_query]
    docs = db.collection(u'cities').where(u'capital', u'==', True).get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # [END get_simple_query]


def get_full_collection():
    db = firestore.Client()
    # [START get_full_collection]
    docs = db.collection(u'cities').get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # [END get_full_collection]


def structure_doc_ref():
    db = firestore.Client()
    # [START structure_doc_ref]
    a_lovelace_ref = db.collection(u'users').document(u'alovelace')
    # [END structure_doc_ref]
    print(a_lovelace_ref)


def structure_collection_ref():
    db = firestore.Client()
    # [START structure_collection_ref]
    users_ref = db.collection(u'users')
    # [END structure_collection_ref]
    print(users_ref)


def structure_doc_ref_alternate():
    db = firestore.Client()
    # [START structure_doc_ref_alternate]
    a_lovelace_ref = db.document(u'users/alovelace')
    # [END structure_doc_ref_alternate]

    return a_lovelace_ref


def structure_subcollection_ref():
    db = firestore.Client()
    # [START structure_subcollection_ref]
    room_a_ref = db.collection(u'rooms').document(u'roomA')
    message_ref = room_a_ref.collection(u'messages').document(u'message1')
    # [END structure_subcollection_ref]
    print(message_ref)


def update_doc():
    db = firestore.Client()
    # [START update_doc]
    city_ref = db.collection(u'cities').document(u'DC')

    # Set the capital field
    city_ref.update({u'capital': True})
    # [END update_doc]


def update_multiple():
    db = firestore.Client()
    # [START update_multiple]
    doc_ref = db.collection(u'cities').document(u'DC')

    doc_ref.update({
        u'name': u'Washington D.C.',
        u'country': u'USA',
        u'capital': True
    })
    # [END update_multiple]


def update_create_if_missing():
    db = firestore.Client()
    # [START update_create_if_missing]
    city_ref = db.collection(u'cities').document(u'BJ')

    city_ref.update({
        u'capital': True
    }, firestore.CreateIfMissingOption(True))
    # [END update_create_if_missing]


def update_nested():
    db = firestore.Client()
    # [START update_nested]
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
    # [END update_nested]


def update_server_timestamp():
    db = firestore.Client()
    # [START update_server_timestamp]
    city_ref = db.collection(u'objects').document(u'some-id')
    city_ref.update({
        u'timestamp': firestore.SERVER_TIMESTAMP
    })
    # [END update_server_timestamp]


def update_data_transaction():
    db = firestore.Client()
    # [START update_data_transaction]
    transaction = db.transaction()
    city_ref = db.collection(u'cities').document(u'SF')

    @firestore.transactional
    def update_in_transaction(transaction, city_ref):
        snapshot = city_ref.get(transaction=transaction)
        transaction.update(city_ref, {
            u'population': snapshot.get(u'population') + 1
        })

    update_in_transaction(transaction, city_ref)
    # [END update_data_transaction]


def update_data_transaction_result():
    db = firestore.Client()
    # [START update_data_transaction_result]
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
    # [END update_data_transaction_result]


def update_data_batch():
    db = firestore.Client()
    # [START update_data_batch]
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
    # [END update_data_batch]


def compound_query_example():
    db = firestore.Client()
    # [START compound_query_example]
    # Create a reference to the cities collection
    cities_ref = db.collection(u'cities')

    # Create a query against the collection
    query_ref = cities_ref.where(u'state', u'==', u'CA')
    # [END compound_query_example]

    return query_ref


def compound_query_simple():
    db = firestore.Client()
    # [START compound_query_simple]
    cities_ref = db.collection(u'cities')

    query = cities_ref.where(u'capital', u'==', True)
    # [END compound_query_simple]

    print(query)


def compound_query_single_clause():
    db = firestore.Client()
    # [START compound_query_single_clause]
    cities_ref = db.collection(u'cities')

    cities_ref.where(u'state', u'==', u'CA')
    cities_ref.where(u'population', u'<', 1000000)
    cities_ref.where(u'name', u'>=', u'San Francisco')
    # [END compound_query_single_clause]


def compound_query_valid_multi_clause():
    db = firestore.Client()
    # [START compound_query_valid_multi_clause]
    cities_ref = db.collection(u'cities')

    sydney_query = cities_ref.where(
        u'state', u'==', u'CO').where(u'name', u'==', u'Denver')
    large_us_cities_query = cities_ref.where(
        u'state', u'==', u'CA').where(u'population', u'>', 1000000)
    # [END compound_query_valid_multi_clause]
    print(sydney_query)
    print(large_us_cities_query)


def compound_query_valid_single_field():
    db = firestore.Client()
    # [START compound_query_valid_single_field]
    cities_ref = db.collection(u'cities')
    cities_ref.where(u'state', u'>=', u'CA').where(u'state', u'<=', u'IN')
    # [END compound_query_valid_single_field]


def compound_query_invalid_multi_field():
    db = firestore.Client()
    # [START compound_query_invalid_multi_field]
    cities_ref = db.collection(u'cities')
    cities_ref.where(
        u'state', u'>=', u'CA').where(u'population', u'>=', 1000000)
    # [END compound_query_invalid_multi_field]


def order_simple_limit():
    db = firestore.Client()
    # [START order_simple_limit]
    db.collection(u'cities').order_by(u'name').limit(3).get()
    # [END order_simple_limit]


def order_simple_limit_desc():
    db = firestore.Client()
    # [START order_simple_limit_desc]
    cities_ref = db.collection(u'cities')
    query = cities_ref.order_by(
        u'name', direction=firestore.Query.DESCENDING).limit(3)
    results = query.get()
    # [END order_simple_limit_desc]
    print(results)


def order_multiple():
    db = firestore.Client()
    # [START order_multiple]
    cities_ref = db.collection(u'cities')
    cities_ref.order_by(u'state').order_by(
        u'population', direction=firestore.Query.DESCENDING)
    # [END order_multiple]


def order_where_limit():
    db = firestore.Client()
    # [START order_where_limit]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(
        u'population', u'>', 2500000).order_by(u'population').limit(2)
    results = query.get()
    # [END order_where_limit]
    print(results)


def order_where_valid():
    db = firestore.Client()
    # [START order_where_valid]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(
        u'population', u'>', 2500000).order_by(u'population')
    results = query.get()
    # [END order_where_valid]
    print(results)


def order_where_invalid():
    db = firestore.Client()
    # [START order_where_invalid]
    cities_ref = db.collection(u'cities')
    query = cities_ref.where(u'population', u'>', 2500000).order_by(u'country')
    results = query.get()
    # [END order_where_invalid]
    print(results)


def cursor_simple_start_at():
    db = firestore.Client()
    # [START cursor_simple_start_at]
    cities_ref = db.collection(u'cities')
    query_start_at = cities_ref.order_by(u'population').start_at({
        u'population': 1000000
    })
    # [END cursor_simple_start_at]

    return query_start_at


def cursor_simple_end_at():
    db = firestore.Client()
    # [START cursor_simple_end_at]
    cities_ref = db.collection(u'cities')
    query_end_at = cities_ref.order_by(u'population').end_at({
        u'population': 1000000
    })
    # [END cursor_simple_end_at]

    return query_end_at


def cursor_paginate():
    db = firestore.Client()
    # [START cursor_paginate]
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
    # [END cursor_paginate]

    return next_query


def cursor_multiple_conditions():
    db = firestore.Client()
    # [START cursor_multiple_conditions]
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
    # [END cursor_multiple_conditions]

    return start_at_name, start_at_name_and_state


def delete_single_doc():
    db = firestore.Client()
    # [START delete_single_doc]
    db.collection(u'cities').document(u'DC').delete()
    # [END delete_single_doc]


def delete_field():
    db = firestore.Client()
    # [START delete_field]
    city_ref = db.collection(u'cities').document(u'BJ')
    city_ref.update({
        u'capital': firestore.DELETE_FIELD
    })
    # [END delete_field]


def delete_full_collection():
    db = firestore.Client()

    # [START delete_full_collection]
    def delete_collection(coll_ref, batch_size):
        docs = coll_ref.limit(10).get()
        deleted = 0

        for doc in docs:
            print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
            doc.reference.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)
    # [END delete_full_collection]

    delete_collection(db.collection(u'cities'), 10)

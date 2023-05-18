# Copyright 2020 Google, Inc.
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


async def quickstart_new_instance():
    # [START firestore_setup_client_create_async]
    from google.cloud import firestore

    # The `project` parameter is optional and represents which project the client
    # will act on behalf of. If not supplied, the client falls back to the default
    # project inferred from the environment.
    db = firestore.AsyncClient(project='my-project-id')
    # [END firestore_setup_client_create_async]

    return db


async def quickstart_add_data_one():
    db = firestore.AsyncClient()
    # [START firestore_setup_dataset_pt1_async]
    doc_ref = db.collection("users").document("alovelace")
    await doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    # [END firestore_setup_dataset_pt1_async]


async def quickstart_add_data_two():
    db = firestore.AsyncClient()
    # [START firestore_setup_dataset_pt2_async]
    doc_ref = db.collection("users").document("aturing")
    await doc_ref.set(
        {"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912}
    )
    # [END firestore_setup_dataset_pt2_async]


async def quickstart_get_collection():
    db = firestore.AsyncClient()
    # [START firestore_quickstart_get_collection_async]
    users_ref = db.collection("users")
    docs = users_ref.stream()

    async for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    # [END firestore_quickstart_get_collection_async]


async def add_from_dict():
    db = firestore.AsyncClient()
    # [START firestore_data_set_from_map_async]
    data = {"name": "Los Angeles", "state": "CA", "country": "USA"}

    # Add a new doc in collection 'cities' with ID 'LA'
    await db.collection("cities").document("LA").set(data)
    # [END firestore_data_set_from_map_async]


async def add_data_types():
    db = firestore.AsyncClient()
    # [START firestore_data_set_from_map_nested_async]
    data = {
        "stringExample": "Hello, World!",
        "booleanExample": True,
        "numberExample": 3.14159265,
        "dateExample": datetime.datetime.now(tz=datetime.timezone.utc),
        "arrayExample": [5, True, "hello"],
        "nullExample": None,
        "objectExample": {"a": 5, "b": True},
    }

    await db.collection("data").document("one").set(data)
    # [END firestore_data_set_from_map_nested_async]


# [START firestore_data_custom_type_definition_async]
class City:
    def __init__(self, name, state, country, capital=False, population=0, regions=[]):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population
        self.regions = regions

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        city = City(source["name"], source["state"], source["country"])

        if "capital" in source:
            city.capital = source["capital"]

        if "population" in source:
            city.population = source["population"]

        if "regions" in source:
            city.regions = source["regions"]

        return city
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {"name": self.name, "state": self.state, "country": self.country}

        if self.capital:
            dest["capital"] = self.capital

        if self.population:
            dest["population"] = self.population

        if self.regions:
            dest["regions"] = self.regions

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return f"City(\
                name={self.name}, \
                country={self.country}, \
                population={self.population}, \
                capital={self.capital}, \
                regions={self.regions}\
            )"

# [END firestore_data_custom_type_definition_async]


async def add_example_data():
    db = firestore.AsyncClient()
    # [START firestore_data_get_dataset_async]
    cities_ref = db.collection("cities")
    await cities_ref.document("BJ").set(
        City("Beijing", None, "China", True, 21500000, ["hebei"]).to_dict()
    )
    await cities_ref.document("SF").set(
        City(
            "San Francisco", "CA", "USA", False, 860000, ["west_coast", "norcal"]
        ).to_dict()
    )
    await cities_ref.document("LA").set(
        City(
            "Los Angeles", "CA", "USA", False, 3900000, ["west_coast", "socal"]
        ).to_dict()
    )
    await cities_ref.document("DC").set(
        City("Washington D.C.", None, "USA", True, 680000, ["east_coast"]).to_dict()
    )
    await cities_ref.document("TOK").set(
        City("Tokyo", None, "Japan", True, 9000000, ["kanto", "honshu"]).to_dict()
    )
    # [END firestore_data_get_dataset_async]


async def add_custom_class_with_id():
    db = firestore.AsyncClient()
    # [START firestore_data_set_from_custom_type_async]
    city = City(name="Los Angeles", state="CA", country="USA")
    await db.collection("cities").document("LA").set(city.to_dict())
    # [END firestore_data_set_from_custom_type_async]


async def add_data_with_id():
    db = firestore.AsyncClient()
    data = {}
    # [START firestore_data_set_id_specified_async]
    await db.collection("cities").document("new-city-id").set(data)
    # [END firestore_data_set_id_specified_async]


async def add_custom_class_generated_id():
    db = firestore.AsyncClient()
    # [START firestore_data_set_id_random_collection_async]
    city = City(name="Tokyo", state=None, country="Japan")
    await db.collection("cities").add(city.to_dict())
    # [END firestore_data_set_id_random_collection_async]


async def add_new_doc():
    db = firestore.AsyncClient()
    # [START firestore_data_set_id_random_document_ref_async]
    new_city_ref = db.collection("cities").document()

    # later...
    await new_city_ref.set(
        {
            # ...
        }
    )
    # [END firestore_data_set_id_random_document_ref_async]


async def get_check_exists():
    db = firestore.AsyncClient()
    # [START firestore_data_get_as_map_async]
    doc_ref = db.collection("cities").document("SF")

    doc = await doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
    else:
        print("No such document!")
    # [END firestore_data_get_as_map_async]


async def get_custom_class():
    db = firestore.AsyncClient()
    # [START firestore_data_get_as_custom_type_async]
    doc_ref = db.collection("cities").document("BJ")

    doc = await doc_ref.get()
    city = City.from_dict(doc.to_dict())
    print(city)
    # [END firestore_data_get_as_custom_type_async]


async def get_simple_query():
    db = firestore.AsyncClient()
    # [START firestore_data_query_async]
    # Note: Use of CollectionRef stream() is prefered to get()
    docs = db.collection("cities").where("capital", "==", True).stream()

    async for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    # [END firestore_data_query_async]


async def array_contains_filter():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_array_contains_async]
    cities_ref = db.collection("cities")

    query = cities_ref.where("regions", "array_contains", "west_coast")
    # [END firestore_query_filter_array_contains_async]
    docs = query.stream()
    async for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")


async def get_full_collection():
    db = firestore.AsyncClient()
    # [START firestore_data_get_all_documents_async]
    docs = db.collection("cities").stream()

    async for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    # [END firestore_data_get_all_documents_async]


async def structure_doc_ref():
    db = firestore.AsyncClient()
    # [START firestore_data_reference_document_async]
    a_lovelace_ref = db.collection("users").document("alovelace")
    # [END firestore_data_reference_document_async]
    print(a_lovelace_ref)


async def structure_collection_ref():
    db = firestore.AsyncClient()
    # [START firestore_data_reference_collection_async]
    users_ref = db.collection("users")
    # [END firestore_data_reference_collection_async]
    print(users_ref)


async def structure_doc_ref_alternate():
    db = firestore.AsyncClient()
    # [START firestore_data_reference_document_path_async]
    a_lovelace_ref = db.document("users/alovelace")
    # [END firestore_data_reference_document_path_async]

    return a_lovelace_ref


async def structure_subcollection_ref():
    db = firestore.AsyncClient()
    # [START firestore_data_reference_subcollection_async]
    room_a_ref = db.collection("rooms").document("roomA")
    message_ref = room_a_ref.collection("messages").document("message1")
    # [END firestore_data_reference_subcollection_async]
    print(message_ref)


async def update_doc():
    db = firestore.AsyncClient()
    await db.collection("cities").document("DC").set(
        City("Washington D.C.", None, "USA", True, 680000, ["east_coast"]).to_dict()
    )
    # [START firestore_data_set_field_async]
    city_ref = db.collection("cities").document("DC")

    # Set the capital field
    await city_ref.update({"capital": True})
    # [END firestore_data_set_field_async]


async def update_doc_array():
    db = firestore.AsyncClient()
    await db.collection("cities").document("DC").set(
        City("Washington D.C.", None, "USA", True, 680000, ["east_coast"]).to_dict()
    )

    # [START firestore_data_set_array_operations_async]
    city_ref = db.collection("cities").document("DC")

    # Atomically add a new region to the 'regions' array field.
    await city_ref.update({"regions": firestore.ArrayUnion(["greater_virginia"])})

    # // Atomically remove a region from the 'regions' array field.
    await city_ref.update({"regions": firestore.ArrayRemove(["east_coast"])})
    # [END firestore_data_set_array_operations_async]
    city = await city_ref.get()
    print(f"Updated the regions field of the DC. {city.to_dict()}")


async def update_multiple():
    db = firestore.AsyncClient()
    await db.collection("cities").document("DC").set(
        City("Washington D.C.", None, "USA", True, 680000, ["east_coast"]).to_dict()
    )

    # [START firestore_update_multiple_async]
    doc_ref = db.collection("cities").document("DC")

    await doc_ref.update({"name": "Washington D.C.", "country": "USA", "capital": True})
    # [END firestore_update_multiple_async]


async def update_create_if_missing():
    db = firestore.AsyncClient()
    # [START firestore_data_set_doc_upsert_async]
    city_ref = db.collection("cities").document("BJ")

    await city_ref.set({"capital": True}, merge=True)
    # [END firestore_data_set_doc_upsert_async]


async def update_nested():
    db = firestore.AsyncClient()
    # [START firestore_data_set_nested_fields_async]
    # Create an initial document to update
    frank_ref = db.collection("users").document("frank")
    await frank_ref.set(
        {
            "name": "Frank",
            "favorites": {"food": "Pizza", "color": "Blue", "subject": "Recess"},
            "age": 12,
        }
    )

    # Update age and favorite color
    await frank_ref.update({"age": 13, "favorites.color": "Red"})
    # [END firestore_data_set_nested_fields_async]


async def update_server_timestamp():
    db = firestore.AsyncClient()
    # [START firestore_data_set_server_timestamp_async]
    city_ref = db.collection("objects").document("some-id")
    await city_ref.update({"timestamp": firestore.SERVER_TIMESTAMP})
    # [END firestore_data_set_server_timestamp_async]


async def update_data_transaction():
    db = firestore.AsyncClient()
    # [START firestore_transaction_document_update_async]
    transaction = db.transaction()
    city_ref = db.collection("cities").document("SF")

    @firestore.async_transactional
    async def update_in_transaction(transaction, city_ref):
        snapshot = await city_ref.get(transaction=transaction)
        transaction.update(city_ref, {"population": snapshot.get("population") + 1})

    await update_in_transaction(transaction, city_ref)
    # [END firestore_transaction_document_update_async]


async def update_data_transaction_result():
    db = firestore.AsyncClient()
    # [START firestore_transaction_document_update_conditional_async]
    transaction = db.transaction()
    city_ref = db.collection("cities").document("SF")

    @firestore.async_transactional
    async def update_in_transaction(transaction, city_ref):
        snapshot = await city_ref.get(transaction=transaction)
        new_population = snapshot.get("population") + 1

        if new_population < 1000000:
            transaction.update(city_ref, {"population": new_population})
            return True
        else:
            return False

    result = await update_in_transaction(transaction, city_ref)
    if result:
        print("Population updated")
    else:
        print("Sorry! Population is too big.")
    # [END firestore_transaction_document_update_conditional_async]


async def update_data_batch():
    db = firestore.AsyncClient()
    # [START firestore_data_batch_writes_async]
    batch = db.batch()

    # Set the data for NYC
    nyc_ref = db.collection("cities").document("NYC")
    batch.set(nyc_ref, {"name": "New York City"})

    # Update the population for SF
    sf_ref = db.collection("cities").document("SF")
    batch.update(sf_ref, {"population": 1000000})

    # Delete DEN
    den_ref = db.collection("cities").document("DEN")
    batch.delete(den_ref)

    # Commit the batch
    await batch.commit()
    # [END firestore_data_batch_writes_async]


async def compound_query_example():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_eq_string_async]
    # Create a reference to the cities collection
    cities_ref = db.collection("cities")

    # Create a query against the collection
    query_ref = cities_ref.where("state", "==", "CA")
    # [END firestore_query_filter_eq_string_async]

    return query_ref


async def compound_query_simple():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_eq_boolean_async]
    cities_ref = db.collection("cities")

    query = cities_ref.where("capital", "==", True)
    # [END firestore_query_filter_eq_boolean_async]

    print(query)


async def compound_query_single_clause():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_single_examples_async]
    cities_ref = db.collection("cities")

    cities_ref.where("state", "==", "CA")
    cities_ref.where("population", "<", 1000000)
    cities_ref.where("name", ">=", "San Francisco")
    # [END firestore_query_filter_single_examples_async]


async def compound_query_valid_multi_clause():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_compound_multi_eq_async]
    cities_ref = db.collection("cities")

    denver_query = cities_ref.where("state", "==", "CO").where("name", "==", "Denver")
    large_us_cities_query = cities_ref.where("state", "==", "CA").where(
        "population", ">", 1000000
    )
    # [END firestore_query_filter_compound_multi_eq_async]
    print(denver_query)
    print(large_us_cities_query)


async def compound_query_valid_single_field():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_range_valid_async]
    cities_ref = db.collection("cities")
    cities_ref.where("state", ">=", "CA").where("state", "<=", "IN")
    # [END firestore_query_filter_range_valid_async]


async def compound_query_invalid_multi_field():
    db = firestore.AsyncClient()
    # [START firestore_query_filter_range_invalid_async]
    cities_ref = db.collection("cities")
    cities_ref.where("state", ">=", "CA").where("population", ">=", 1000000)
    # [END firestore_query_filter_range_invalid_async]


async def order_simple_limit():
    db = firestore.AsyncClient()
    # [START firestore_order_simple_limit_async]
    db.collection("cities").order_by("name").limit(3).stream()
    # [END firestore_order_simple_limit_async]


async def order_simple_limit_desc():
    db = firestore.AsyncClient()
    # [START firestore_query_order_desc_limit_async]
    cities_ref = db.collection("cities")
    query = cities_ref.order_by("name", direction=firestore.Query.DESCENDING).limit(3)
    results = query.stream()
    # [END firestore_query_order_desc_limit_async]
    print(results)


async def order_multiple():
    db = firestore.AsyncClient()
    # [START firestore_query_order_multi_async]
    cities_ref = db.collection("cities")
    cities_ref.order_by("state").order_by(
        "population", direction=firestore.Query.DESCENDING
    )
    # [END firestore_query_order_multi_async]


async def order_where_limit():
    db = firestore.AsyncClient()
    # [START firestore_query_order_limit_field_valid_async]
    cities_ref = db.collection("cities")
    query = cities_ref.where("population", ">", 2500000).order_by("population").limit(2)
    results = query.stream()
    # [END firestore_query_order_limit_field_valid_async]
    print([d async for d in results])


async def order_limit_to_last():
    db = firestore.AsyncClient()
    # [START firestore_query_order_limit_async]
    cities_ref = db.collection("cities")
    query = cities_ref.order_by("name").limit_to_last(2)
    results = await query.get()
    # [END firestore_query_order_limit_async]
    print(results)


async def order_where_valid():
    db = firestore.AsyncClient()
    # [START firestore_query_order_with_filter_async]
    cities_ref = db.collection("cities")
    query = cities_ref.where("population", ">", 2500000).order_by("population")
    results = query.stream()
    # [END firestore_query_order_with_filter_async]
    print([d async for d in results])


async def order_where_invalid():
    db = firestore.AsyncClient()
    # [START firestore_query_order_field_invalid_async]
    cities_ref = db.collection("cities")
    query = cities_ref.where("population", ">", 2500000).order_by("country")
    results = query.stream()
    # [END firestore_query_order_field_invalid_async]
    print(results)


async def cursor_simple_start_at():
    db = firestore.AsyncClient()
    # [START firestore_query_cursor_start_at_field_value_single_async]
    cities_ref = db.collection("cities")
    query_start_at = cities_ref.order_by("population").start_at({"population": 1000000})
    # [END firestore_query_cursor_start_at_field_value_single_async]

    return query_start_at


async def cursor_simple_end_at():
    db = firestore.AsyncClient()
    # [START firestore_query_cursor_end_at_field_value_single_async]
    cities_ref = db.collection("cities")
    query_end_at = cities_ref.order_by("population").end_at({"population": 1000000})
    # [END firestore_query_cursor_end_at_field_value_single_async]

    return query_end_at


async def snapshot_cursors():
    db = firestore.AsyncClient()
    # [START firestore_query_cursor_start_at_document_async]
    doc_ref = db.collection("cities").document("SF")

    snapshot = await doc_ref.get()
    start_at_snapshot = (
        db.collection("cities").order_by("population").start_at(snapshot)
    )
    # [END firestore_query_cursor_start_at_document_async]
    results = start_at_snapshot.limit(10).stream()
    async for doc in results:
        print(f"{doc.id}")

    return results


async def cursor_paginate():
    db = firestore.AsyncClient()
    # [START firestore_query_cursor_pagination_async]
    cities_ref = db.collection("cities")
    first_query = cities_ref.order_by("population").limit(3)

    # Get the last document from the results
    docs = [d async for d in first_query.stream()]
    last_doc = list(docs)[-1]

    # Construct a new query starting at this document
    # Note: this will not have the desired effect if
    # multiple cities have the exact same population value
    last_pop = last_doc.to_dict()["population"]

    next_query = (
        cities_ref.order_by("population").start_after({"population": last_pop}).limit(3)
    )
    # Use the query for pagination
    # ...
    # [END firestore_query_cursor_pagination_async]

    return next_query


async def cursor_multiple_conditions():
    db = firestore.AsyncClient()
    # [START firestore_query_cursor_start_at_field_value_multi_async]
    start_at_name = (
        db.collection("cities")
        .order_by("name")
        .order_by("state")
        .start_at({"name": "Springfield"})
    )

    start_at_name_and_state = (
        db.collection("cities")
        .order_by("name")
        .order_by("state")
        .start_at({"name": "Springfield", "state": "Missouri"})
    )
    # [END firestore_query_cursor_start_at_field_value_multi_async]

    return start_at_name, start_at_name_and_state


async def delete_single_doc():
    db = firestore.AsyncClient()
    # [START firestore_data_delete_doc_async]
    await db.collection("cities").document("DC").delete()
    # [END firestore_data_delete_doc_async]


async def delete_field():
    db = firestore.AsyncClient()
    # [START firestore_data_delete_field_async]
    city_ref = db.collection("cities").document("BJ")
    await city_ref.update({"capital": firestore.DELETE_FIELD})
    # [END firestore_data_delete_field_async]


async def delete_full_collection():
    db = firestore.AsyncClient()

    # [START firestore_data_delete_collection_async]
    async def delete_collection(coll_ref, batch_size):
        docs = coll_ref.limit(batch_size).stream()
        deleted = 0

        async for doc in docs:
            print(f"Deleting doc {doc.id} => {doc.to_dict()}")
            await doc.reference.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)

    # [END firestore_data_delete_collection_async]

    await delete_collection(db.collection("cities"), 10)
    await delete_collection(db.collection("data"), 10)
    await delete_collection(db.collection("objects"), 10)
    await delete_collection(db.collection("users"), 10)


async def collection_group_query(db):
    # [START firestore_query_collection_group_dataset_async]
    cities = db.collection("cities")

    sf_landmarks = cities.document("SF").collection("landmarks")
    await sf_landmarks.document().set({"name": "Golden Gate Bridge", "type": "bridge"})
    await sf_landmarks.document().set({"name": "Legion of Honor", "type": "museum"})
    la_landmarks = cities.document("LA").collection("landmarks")
    await la_landmarks.document().set({"name": "Griffith Park", "type": "park"})
    await la_landmarks.document().set({"name": "The Getty", "type": "museum"})
    dc_landmarks = cities.document("DC").collection("landmarks")
    await dc_landmarks.document().set({"name": "Lincoln Memorial", "type": "memorial"})
    await dc_landmarks.document().set(
        {"name": "National Air and Space Museum", "type": "museum"}
    )
    tok_landmarks = cities.document("TOK").collection("landmarks")
    await tok_landmarks.document().set({"name": "Ueno Park", "type": "park"})
    await tok_landmarks.document().set(
        {"name": "National Museum of Nature and Science", "type": "museum"}
    )
    bj_landmarks = cities.document("BJ").collection("landmarks")
    await bj_landmarks.document().set({"name": "Jingshan Park", "type": "park"})
    await bj_landmarks.document().set(
        {"name": "Beijing Ancient Observatory", "type": "museum"}
    )
    # [END firestore_query_collection_group_dataset_async]

    # [START firestore_query_collection_group_filter_eq_async]
    museums = db.collection_group("landmarks").where("type", "==", "museum")
    docs = museums.stream()
    async for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    # [END firestore_query_collection_group_filter_eq_async]
    return docs


async def array_contains_any_queries(db):
    # [START firestore_query_filter_array_contains_any_async]
    cities_ref = db.collection("cities")

    query = cities_ref.where(
        "regions", "array_contains_any", ["west_coast", "east_coast"]
    )
    return query
    # [END firestore_query_filter_array_contains_any_async]


async def in_query_without_array(db):
    # [START firestore_query_filter_in_async]
    cities_ref = db.collection("cities")

    query = cities_ref.where("country", "in", ["USA", "Japan"])
    return query
    # [END firestore_query_filter_in_async]


async def in_query_with_array(db):
    # [START firestore_query_filter_in_with_array_async]
    cities_ref = db.collection("cities")

    query = cities_ref.where("regions", "in", [["west_coast"], ["east_coast"]])
    return query
    # [END firestore_query_filter_in_with_array_async]


async def update_document_increment(db):
    # [START firestore_data_set_numeric_increment_async]
    washington_ref = db.collection("cities").document("DC")

    washington_ref.update({"population": firestore.Increment(50)})
    # [END firestore_data_set_numeric_increment_async]


async def list_document_subcollections():
    db = firestore.AsyncClient()
    # [START firestore_data_get_sub_collections_async]
    collections = db.collection("cities").document("SF").collections()
    async for collection in collections:
        async for doc in collection.stream():
            print(f"{doc.id} => {doc.to_dict()}")
    # [END firestore_data_get_sub_collections_async]

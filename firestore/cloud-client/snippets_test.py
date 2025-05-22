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
from datetime import datetime
import json
import os
import re
import uuid

from google.cloud import firestore
import pytest

import snippets

# TODO(developer): Before running these tests locally,
# set your FIRESTORE_PROJECT env variable
# and create a Database named `(default)`

os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]


class TestFirestoreClient(firestore.Client):
    def __init__(self, add_unique_string: bool = True, *args, **kwargs):
        self._UNIQUE_STRING = UNIQUE_STRING
        self._super = super()
        self._super.__init__(*args, **kwargs)
        self.add_unique_string = add_unique_string

    def collection(self, collection_name: str, *args, **kwargs):
        if (
            self.add_unique_string and self._UNIQUE_STRING not in collection_name
        ):  # subcollection overwrite prevention
            collection_name = self.unique_collection_name(collection_name)
        return self._super.collection(collection_name, *args, **kwargs)

    def unique_collection_name(self, collection_name: str) -> str:
        return f"{collection_name}-{self._UNIQUE_STRING}"


snippets.firestore.Client = TestFirestoreClient


@pytest.fixture(scope="function")
def db():
    client = TestFirestoreClient()
    yield client
    # Cleanup
    try:
        all_collections = client.collections()
        test_collections_base = [
            "cities",
            "users",
            "data",
            "objects",
            "rooms",
            "landmarks",
        ]
        for collection in all_collections:
            if any(
                collection.id.startswith(base_name)
                for base_name in test_collections_base
            ):
                for doc in collection.stream():
                    doc.reference.delete()
    except Exception as e:
        raise f"Cleanup failed: {e}"


@pytest.fixture(scope="function")
def db_no_unique_string():
    client = TestFirestoreClient(add_unique_string=False)
    yield client
    # Cleanup
    test_collections = ["cities", "employees"]
    for collection in test_collections:
        try:
            for doc in client.collection(collection).stream():
                doc.reference.delete()
        except Exception as e:
            raise f"Cleanup failed: {e}"


def test_quickstart_new_instance():
    client = snippets.quickstart_new_instance()
    assert client.project == "my-project-id"


def test_quickstart_add_data_two(db):
    snippets.quickstart_add_data_two()
    doc_ref = db.collection("users").document("aturing")
    doc = doc_ref.get()
    assert doc.exists
    assert doc.to_dict() == {
        "first": "Alan",
        "middle": "Mathison",
        "last": "Turing",
        "born": 1912,
    }


def test_quickstart_get_collection(db, capsys):
    snippets.quickstart_add_data_one()
    snippets.quickstart_add_data_two()
    snippets.quickstart_get_collection()  # This function prints output
    out, _ = capsys.readouterr()
    # Parse each line as JSON and check for the presence of required data
    output_lines = out.strip().replace("'", '"').split("\n")
    expected_data = [
        {"first": "Ada", "last": "Lovelace", "born": 1815},
        {"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912},
    ]
    # Convert all output lines to JSON objects
    output_data = [json.loads(line.split(" => ")[1]) for line in output_lines]

    # Check each expected item is in output data
    for expected_item in expected_data:
        assert any(
            expected_item == item for item in output_data
        ), f"Missing or incorrect data: {expected_item}"


def test_add_from_dict(db):
    snippets.add_from_dict()
    doc_ref = db.collection("cities").document("LA")
    doc = doc_ref.get()
    assert doc.exists
    assert doc.to_dict() == {"name": "Los Angeles", "state": "CA", "country": "USA"}


def test_add_data_types(db):
    snippets.add_data_types()
    doc_ref = db.collection("data").document("one")
    doc = doc_ref.get()
    assert doc.exists
    data = doc.to_dict()
    assert data["stringExample"] == "Hello, World!"
    assert data["booleanExample"] is True
    assert isinstance(data["dateExample"], datetime)


def test_quickstart_add_data_one(db):
    snippets.quickstart_add_data_one()  # Assume it uses db internally
    doc_ref = db.collection("users").document("alovelace")
    doc = doc_ref.get()
    assert doc.exists
    assert doc.to_dict() == {"first": "Ada", "last": "Lovelace", "born": 1815}


def test_add_example_data(db):
    snippets.add_example_data()
    cities = ["BJ", "SF", "LA", "DC", "TOK"]
    for city_id in cities:
        doc_ref = db.collection("cities").document(city_id)
        doc = doc_ref.get()
        assert doc.exists


def test_array_contains_any_queries(db):
    # Setup cities with regions
    db.collection("cities").document("City1").set(
        {"regions": ["west_coast", "east_coast"]}
    )
    db.collection("cities").document("City2").set({"regions": ["east_coast"]})
    query = snippets.array_contains_any_queries(db)
    results = list(query.stream())
    assert len(results) >= 2


def test_query_filter_in_query_without_array(db):
    db.collection("cities").document("Tokyo").set({"country": "Japan"})
    db.collection("cities").document("SF").set({"country": "USA"})
    result = snippets.in_query_without_array(db)
    results = list(result.stream())
    assert len(results) == 2


def test_query_filter_in_query_with_array(db):
    db.collection("cities").document("LA").set({"regions": ["west_coast"]})
    db.collection("cities").document("NYC").set({"regions": ["east_coast"]})
    result = snippets.in_query_with_array(db)
    results = list(result.stream())
    assert len(results) >= 2


def test_not_in_query(db):
    db.collection("cities").document("LA").set({"country": "USA"})
    db.collection("cities").document("Tokyo").set({"country": "Japan"})
    db.collection("cities").document("Saskatoon").set({"country": "Canada"})
    result = snippets.not_in_query(db)
    results = list(result.stream())
    assert len(results) == 1
    assert results[0].to_dict()["country"] == "Canada"


def test_not_equal_query(db_no_unique_string):
    db = db_no_unique_string
    db.collection("cities").document("Ottawa").set(
        {"capital": True, "country": "Canada"}
    )
    db.collection("cities").document("Kyoto").set(
        {"capital": False, "country": "Japan"}
    )
    db.collection("cities").document("LA").set({"capital": False, "country": "USA"})
    result = snippets.not_equal_query(db)
    results = list(result.stream())
    assert len(results) == 1
    assert results[0].to_dict()["country"] == "Canada"


def test_add_custom_class_with_id(db):
    snippets.add_custom_class_with_id()
    doc_ref = db.collection("cities").document("LA")
    doc = doc_ref.get()
    assert doc.exists
    assert doc.to_dict() == {
        "name": "Los Angeles",
        "state": "CA",
        "country": "USA",
    }


def test_add_data_with_id(db):
    snippets.add_custom_class_with_id()
    doc_ref = db.collection("cities").document("LA")
    doc = doc_ref.get()
    assert doc.exists
    assert doc.to_dict() == {"name": "Los Angeles", "state": "CA", "country": "USA"}


def test_add_custom_class_generated_id(capsys):
    snippets.add_custom_class_generated_id()
    out, _ = capsys.readouterr()
    assert "Added document with id" in out


def test_add_new_doc():
    snippets.add_new_doc()  # No data to assert, we are just testing the call


def test_get_simple_query(db):
    db.collection("cities").document("NY").set({"capital": True})
    snippets.get_simple_query()  # Assuming function prints or logs output
    query = db.collection("cities").where("capital", "==", True)
    docs = list(query.stream())
    assert len(docs) == 1
    assert docs[0].to_dict()["capital"] is True


def test_array_contains_filter(db):
    db.collection("cities").document("LA").set({"regions": ["west_coast", "socal"]})
    snippets.array_contains_filter()
    query = db.collection("cities").where("regions", "array_contains", "west_coast")
    docs = list(query.stream())
    assert len(docs) == 1
    assert "west_coast" in docs[0].to_dict()["regions"]


def test_get_full_collection(db):
    db.collection("cities").document("SF").set({"name": "San Francisco"})
    snippets.get_full_collection()
    docs = list(db.collection("cities").stream())
    assert len(docs) > 0


def test_get_custom_class(db):
    city_data = {
        "name": "Beijing",
        "state": "BJ",
        "country": "China",
        "population": 21500000,
        "capital": True,
    }
    db.collection("cities").document("BJ").set(city_data)
    snippets.get_custom_class()
    doc_ref = db.collection("cities").document("BJ")
    doc = doc_ref.get()
    city = snippets.City.from_dict(doc.to_dict())
    assert city.name == "Beijing"
    assert city.capital is True


def test_get_check_exists(db):
    db.collection("cities").document("SF").set({"name": "San Francisco"})
    snippets.get_check_exists()
    doc_ref = db.collection("cities").document("SF")
    doc = doc_ref.get()
    assert doc.exists


def test_structure_subcollection_ref(db):
    db.collection("rooms").document("roomA").collection("messages").document(
        "message1"
    ).set({"text": "Hello"})
    snippets.structure_subcollection_ref()
    doc_ref = (
        db.collection("rooms")
        .document("roomA")
        .collection("messages")
        .document("message1")
    )
    assert doc_ref.get().exists


def test_structure_collection_ref(db):
    snippets.structure_collection_ref()
    col_ref = db.collection("users")
    assert isinstance(col_ref, firestore.CollectionReference)


def test_structure_doc_ref_alternate(db):
    doc_ref = snippets.structure_doc_ref_alternate()
    assert isinstance(doc_ref, firestore.DocumentReference)
    assert doc_ref.id == "alovelace"


def test_structure_doc_ref(db):
    snippets.structure_doc_ref()
    doc_ref = db.collection("users").document("alovelace")
    assert isinstance(doc_ref, firestore.DocumentReference)


def test_update_create_if_missing(db):
    snippets.update_create_if_missing()
    doc_ref = db.collection("cities").document("BJ")
    doc = doc_ref.get()
    assert doc.to_dict()["capital"] is True


def test_update_doc(db):
    db.collection("cities").document("DC").set({"name": "Washington D.C."})
    snippets.update_doc()
    doc_ref = db.collection("cities").document("DC")
    doc = doc_ref.get()
    assert doc.to_dict()["capital"] is True


def test_update_doc_array(capsys):
    snippets.update_doc_array()
    out, _ = capsys.readouterr()
    assert "greater_virginia" in out


def test_update_multiple(db):
    db.collection("cities").document("DC").set({"name": "Washington"})
    snippets.update_multiple()
    doc_ref = db.collection("cities").document("DC")
    doc = doc_ref.get()
    assert doc.to_dict()["name"] == "Washington D.C."
    assert doc.to_dict()["capital"] is True


def test_update_server_timestamp(db):
    db.collection("objects").document("some-id").set({"timestamp": 0})
    snippets.update_server_timestamp()
    doc_ref = db.collection("objects").document("some-id")
    doc = doc_ref.get()
    assert "timestamp" in doc.to_dict()


def test_update_data_transaction(db):
    db.collection("cities").document("SF").set({"population": 1})
    snippets.update_data_transaction()
    doc_ref = db.collection("cities").document("SF")
    doc = doc_ref.get()
    assert doc.to_dict()["population"] == 2


def test_update_data_transaction_result(db, capsys):
    db.collection("cities").document("SF").set({"population": 1})
    snippets.update_data_transaction_result()
    out, _ = capsys.readouterr()
    assert "Population updated" in out


def test_update_data_batch(db):
    db.collection("cities").document("NYC").set({"name": "New York City"})
    db.collection("cities").document("SF").set({"population": 850000})
    db.collection("cities").document("DEN").set({"name": "Denver"})
    snippets.update_data_batch()
    nyc_ref = db.collection("cities").document("NYC")
    sf_ref = db.collection("cities").document("SF")
    den_ref = db.collection("cities").document("DEN")
    assert nyc_ref.get().exists
    assert sf_ref.get().to_dict()["population"] == 1000000
    assert not den_ref.get().exists


def test_update_nested(db):
    db.collection("users").document("frank").set(
        {"name": "Frank", "favorites": {"color": "Blue"}, "age": 12}
    )
    snippets.update_nested()
    doc_ref = db.collection("users").document("frank")
    doc = doc_ref.get()
    assert doc.to_dict()["age"] == 13
    assert doc.to_dict()["favorites"]["color"] == "Red"


def test_compound_query_example(db):
    cities = [
        {"name": "Los Angeles", "state": "CA"},
        {"name": "San Francisco", "state": "CA"},
        {"name": "New York", "state": "NY"},
        {"name": "Miami", "state": "FL"},
        {"name": "San Diego", "state": "CA"},
    ]
    for city in cities:
        db.collection("cities").add(city)

    query_ref = snippets.compound_query_example()
    results = list(query_ref.stream())

    assert len(results) >= 3, "Should return at least three cities from CA"
    for doc in results:
        assert doc.to_dict()["state"] == "CA"


def test_compound_query_valid_multi_clause(db_no_unique_string, capsys):
    cities = [
        {"name": "Denver", "state": "CO", "population": 716492},
        {"name": "Los Angeles", "state": "CA", "population": 3979576},
        {"name": "San Diego", "state": "CA", "population": 1425976},
        {"name": "San Francisco", "state": "CA", "population": 881549},
        {"name": "Colorado Springs", "state": "CO", "population": 478961},
    ]
    for city in cities:
        db_no_unique_string.collection("cities").add(city)
    denver_query, large_us_cities_query = snippets.compound_query_valid_multi_clause()
    denver_results = list(denver_query.stream())
    assert len(denver_results) == 1, "Should return exactly one city for Denver"
    assert (
        denver_results[0].to_dict()["name"] == "Denver"
    ), "The city returned should be Denver"

    large_cities_results = list(large_us_cities_query.stream())
    assert (
        len(large_cities_results) >= 2
    ), "Should return at least two large cities in CA"

    for city in large_cities_results:
        assert city.to_dict()["state"] == "CA", "City should be in California"
        assert (
            city.to_dict()["population"] > 1000000
        ), "City should have a population greater than 1,000,000"


def test_compound_query_simple(capsys):
    snippets.compound_query_simple()
    out, _ = capsys.readouterr()
    assert re.search("google.cloud.firestore_v1.query.Query", out)


def test_compound_query_invalid_multi_field():
    try:
        snippets.compound_query_invalid_multi_field()
        assert False  # Should not reach here if the query is invalid
    except Exception:
        assert True


def test_compound_query_single_clause():
    try:
        snippets.compound_query_single_clause()
        assert True
    except Exception:
        assert False


def test_compound_query_valid_single_field():
    try:
        snippets.compound_query_valid_single_field()
        assert True
    except Exception:
        assert False


def test_order_simple_limit(db):
    cities = [
        {"name": "Beijing"},
        {"name": "Auckland"},
        {"name": "Cairo"},
        {"name": "Denver"},
        {"name": "Edinburgh"},
    ]
    for city in cities:
        db.collection("cities").add(city)
    results = snippets.order_simple_limit()
    results_list = list(results)
    assert len(results_list) == 3

    expected_names = [
        "Auckland",
        "Beijing",
        "Cairo",
    ]
    actual_names = [doc.to_dict()["name"] for doc in results_list]
    assert actual_names == expected_names


def test_order_simple_limit_desc(db):
    cities = [
        {"name": "Springfield"},
        {"name": "Shelbyville"},
        {"name": "Ogdenville"},
        {"name": "North Haverbrook"},
        {"name": "Capital City"},
    ]
    for city in cities:
        db.collection("cities").add(city)

    results = snippets.order_simple_limit_desc()

    results_list = list(results)
    assert len(results_list) == 3

    expected_names = [
        "Springfield",
        "Shelbyville",
        "Ogdenville",
    ]  # These should be the names in correct order
    actual_names = [doc.to_dict()["name"] for doc in results_list]
    assert actual_names == expected_names


def test_order_multiple(db_no_unique_string):
    cities = [
        {"name": "CityA", "state": "A", "population": 500000},
        {"name": "CityB", "state": "B", "population": 1500000},
        {"name": "CityC", "state": "A", "population": 200000},
        {"name": "CityD", "state": "B", "population": 1200000},
        {"name": "CityE", "state": "C", "population": 300000},
    ]
    for city in cities:
        db_no_unique_string.collection("cities").add(city)

    query = snippets.order_multiple()
    results = list(query.stream())

    assert len(results) > 0
    last_state = None
    last_population = float("inf")
    for doc in results:
        data = doc.to_dict()
        state, population = data["state"], data["population"]
        if last_state is not None:
            if last_state > state or (
                last_state == state and last_population < population
            ):
                pytest.fail("Cities are not in the correct order")
        last_state, last_population = state, population


def test_order_where_limit(db):
    cities = [
        {"name": "Bigburg", "population": 3000000},
        {"name": "Megapolis", "population": 4500000},
        {"name": "Midtown", "population": 1000000},
        {"name": "Gigacity", "population": 5000000},
        {"name": "Smallville", "population": 500000},
    ]
    for city in cities:
        db.collection("cities").add(city)
    results = snippets.order_where_limit()

    results_list = list(results)
    assert len(results_list) == 2

    expected_populations = [3000000, 4500000]
    actual_populations = [doc.to_dict()["population"] for doc in results_list]
    assert actual_populations == expected_populations


def test_order_limit_to_last(db):
    cities = [
        {"name": "Midtown"},
        {"name": "Gigacity"},
        {"name": "Smallville"},
        {"name": "Bigburg"},
        {"name": "Megapolis"},
    ]
    for city in cities:
        db.collection("cities").add(city)
    results = snippets.order_limit_to_last()
    results_list = list(results)
    assert len(results_list) == 2, "Should return exactly two cities"
    expected_names = ["Midtown", "Smallville"]  # last 2 in ordered by "name"
    actual_names = [doc.to_dict()["name"] for doc in results_list]
    assert (
        actual_names == expected_names
    ), f"Expected city names {expected_names}, but got {actual_names}"


def test_order_where_invalid(db):
    cities = [
        {"name": "Midtown", "population": 500000},
        {"name": "Gigacity", "population": 5000000},
        {"name": "Smallville", "population": 10000},
        {"name": "Bigburg", "population": 800000},
        {"name": "Megapolis", "population": 1500000},
    ]
    for city in cities:
        db.collection("cities").add(city)
    query_stream = snippets.order_where_invalid()
    results = list(query_stream)
    assert len(results) == 0


def test_order_where_valid(db):
    cities = [
        {"name": "Gigacity", "population": 5000000},
        {"name": "Smallville", "population": 10000},
        {"name": "Bigburg", "population": 800000},
        {"name": "Midtown", "population": 500000},
        {"name": "Megapolis", "population": 1500000},
    ]
    for city in cities:
        db.collection("cities").add(city)
    query_stream = snippets.order_where_valid()
    results = list(query_stream)
    assert len(results) == 1


def test_cursor_simple_start_at(db):
    cities = [
        {"name": "Smallville", "population": 10000},
        {"name": "Bigburg", "population": 800000},
        {"name": "Midtown", "population": 500000},
        {"name": "Megapolis", "population": 1500000},
        {"name": "Gigacity", "population": 5000000},
    ]
    for city in cities:
        db.collection("cities").add(city)
    query_start_at = snippets.cursor_simple_start_at()
    results = list(query_start_at.stream())
    assert len(results) == 2


def test_cursor_simple_end_at(db):
    cities = [
        {"name": "Smallville", "population": 10000},
        {"name": "Midtown", "population": 500000},
        {"name": "Bigburg", "population": 800000},
        {"name": "Megapolis", "population": 1500000},
        {"name": "Gigacity", "population": 5000000},
    ]
    for city in cities:
        db.collection("cities").add(city)
    query_end_at = snippets.cursor_simple_end_at()
    results = list(query_end_at.stream())
    assert len(results) == 3


def test_snapshot_cursors(db):
    cities = [
        {"name": "SF", "population": 881549},
        {"name": "LA", "population": 3979576},
        {"name": "SD", "population": 1425976},
    ]
    for city in cities:
        db.collection("cities").document(city["name"]).set(city)
    results = snippets.snapshot_cursors()

    results_list = list(results)
    assert len(results_list) > 0

    expected_first_city = "SF"
    actual_first_city = results_list[0].to_dict()["name"]
    assert actual_first_city == expected_first_city


def test_cursor_paginate(db):
    cities = [
        {"name": "Springfield", "population": 30000},
        {"name": "Shelbyville", "population": 40000},
        {"name": "Ogdenville", "population": 15000},
        {"name": "North Haverbrook", "population": 50000},
        {"name": "Capital City", "population": 120000},
    ]
    for city in cities:
        db.collection("cities").add(city)

    next_query = snippets.cursor_paginate()
    results = list(next_query.stream())

    expected_population = [
        50000,
        120000,
    ]  # Expected results based on initial data setup and population ordering
    actual_populations = [doc.to_dict()["population"] for doc in results]
    assert actual_populations == expected_population


def test_cursor_multiple_conditions(db_no_unique_string):
    cities = [
        {"name": "Springfield", "state": "Illinois"},
        {"name": "Springfield", "state": "Missouri"},
        {"name": "Chicago", "state": "Illinois"},
    ]
    for city in cities:
        db_no_unique_string.collection("cities").add(city)
    start_at_name, start_at_name_and_state = snippets.cursor_multiple_conditions()
    start_at_name_results = list(start_at_name.stream())
    start_at_name_and_state_results = list(start_at_name_and_state.stream())

    assert len(start_at_name_results) >= 2
    assert any(
        doc.to_dict()["state"] == "Missouri" for doc in start_at_name_and_state_results
    )
    assert any(
        doc.to_dict()["name"] == "Springfield"
        for doc in start_at_name_and_state_results
    )


@pytest.mark.flaky(max_runs=3)
def test_listen_document(capsys):
    snippets.listen_document()
    out, _ = capsys.readouterr()
    assert "Received document snapshot: SF" in out


@pytest.mark.flaky(max_runs=3)
def test_listen_multiple(capsys):
    snippets.listen_multiple()
    out, _ = capsys.readouterr()
    assert "Current cities in California:" in out
    assert "SF" in out


@pytest.mark.flaky(max_runs=3)
def test_listen_for_changes(capsys):
    snippets.listen_for_changes()
    out, _ = capsys.readouterr()
    assert "New city: MTV" in out
    assert "Modified city: MTV" in out
    assert "Removed city: MTV" in out


def test_delete_single_doc(db):
    city_ref = db.collection("cities").document("DC")
    city_ref.set({"name": "Washington DC", "capital": True})
    snippets.delete_single_doc()
    doc = city_ref.get()
    assert not doc.exists, "The document should be deleted."


def test_delete_field(db):
    city_ref = db.collection("cities").document("BJ")
    city_ref.set({"capital": True})
    snippets.delete_field()
    doc = city_ref.get()
    assert "capital" not in doc.to_dict()


def test_delete_full_collection(db):
    assert list(db.collection("cities").stream()) == []

    for i in range(5):
        db.collection("cities").document(f"City{i}").set({"name": f"CityName{i}"})
    assert len(list(db.collection("cities").stream())) == 5

    snippets.delete_full_collection()
    assert list(db.collection("cities").stream()) == []


@pytest.mark.skip(
    reason="Dependant on a composite index being created,"
    "however creation of the index is dependent on"
    "having the admin client and definition integrated"
    "into the test setup"
)
# TODO: b/132092178
def test_collection_group_query(db):
    museum_docs = snippets.collection_group_query(db)
    names = {museum.name for museum in museum_docs}
    assert names == {
        "Legion of Honor",
        "The Getty",
        "National Air and Space Museum",
        "National Museum of Nature and Science",
        "Beijing Ancient Observatory",
    }


def test_list_document_subcollections(db, capsys):
    ref = (
        db.collection("cities")
        .document("SF")
        .collection("landmarks")
        .document("GoldenGate")
    )
    ref.set({"type": "Bridge"})

    # res = city_ref.get()
    snippets.list_document_subcollections()
    out, _ = capsys.readouterr()
    assert "GoldenGate => {'type': 'Bridge'}" in out


def test_create_and_build_bundle():
    bundle, buffer = snippets.create_and_build_bundle()
    assert "latest-stories-query" in bundle.named_queries


def test_regional_endpoint(db):
    cities = [
        {"name": "Seattle"},
        {"name": "Portland"},
    ]
    for city in cities:
        db.collection("cities").add(city)

    snippets.regional_endpoint()
    cities_query = snippets.regional_endpoint()

    cities_list = list(cities_query)
    assert len(cities_list) == 2


def test_query_filter_compound_multi_ineq(db_no_unique_string):
    db = db_no_unique_string
    cities = [
        {"name": "SF", "state": "CA", "population": 1_000_000, "density": 10_000},
        {"name": "LA", "state": "CA", "population": 5_000_000, "density": 8_000},
        {"name": "DC", "state": "WA", "population": 700_000, "density": 9_000},
        {"name": "NYC", "state": "NY", "population": 8_000_000, "density": 12_000},
        {"name": "SEA", "state": "WA", "population": 800_000, "density": 7_000},
    ]
    for city in cities:
        db.collection("cities").add(city)
    query = snippets.query_filter_compound_multi_ineq()
    results = list(query.stream())
    assert len(results) == 1
    assert results[0].to_dict()["name"] == "LA"


def test_query_indexing_considerations(db_no_unique_string):
    db = db_no_unique_string
    emplyees = [
        {"name": "Alice", "salary": 100_000, "experience": 10},
        {"name": "Bob", "salary": 80_000, "experience": 2},
        {"name": "Charlie", "salary": 120_000, "experience": 10},
        {"name": "David", "salary": 90_000, "experience": 3},
        {"name": "Eve", "salary": 110_000, "experience": 9},
        {"name": "Joe", "salary": 110_000, "experience": 7},
        {"name": "Mallory", "salary": 200_000, "experience": 0},
    ]
    for employee in emplyees:
        db.collection("employees").add(employee)
    query = snippets.query_indexing_considerations()
    results = list(query.stream())
    # should contain employees salary > 100_000 sorted by salary and experience
    assert len(results) == 3
    assert results[0].to_dict()["name"] == "Joe"
    assert results[1].to_dict()["name"] == "Eve"
    assert results[2].to_dict()["name"] == "Charlie"


def test_query_order_fields(db):
    emplyees = [
        {"name": "Alice", "salary": 100_000, "experience": 10},
        {"name": "Bob", "salary": 80_000, "experience": 2},
        {"name": "Charlie", "salary": 120_000, "experience": 10},
        {"name": "David", "salary": 90_000, "experience": 3},
        {"name": "Eve", "salary": 110_000, "experience": 9},
        {"name": "Joe", "salary": 110_000, "experience": 7},
        {"name": "Mallory", "salary": 200_000, "experience": 0},
    ]
    for employee in emplyees:
        db.collection("employees").add(employee)
    results = snippets.query_order_fields()
    assert len(results) == 4
    assert results[0].to_dict()["name"] == "Mallory"
    assert results[1].to_dict()["name"] == "Joe"
    assert results[2].to_dict()["name"] == "Eve"
    assert results[3].to_dict()["name"] == "Charlie"

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud import datastore
from google.cloud.datastore.vector import Vector

from vector_search import store_vectors
from vector_search import vector_search_basic
from vector_search import vector_search_distance_result_field
from vector_search import vector_search_distance_threshold
from vector_search import vector_search_prefilter


os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_store_vectors():
    client = store_vectors()

    results = client.query("coffee-beans", limit=5).fetch()

    assert len(list(results)) == 1


def add_coffee_beans_data(db):
    entity1 = datastore.Entity(db.key("coffee-beans", "Arabica"))
    entity1.update({"embedding_field": Vector([10.0, 1.0, 2.0]), "color": "red"})
    entity2 = datastore.Entity(db.key("coffee-beans", "Robusta"))
    entity2.update({"embedding_field": Vector([4.0, 1.0, 2.0]), "color": ""})
    entity3 = datastore.Entity(db.key("coffee-beans", "Excelsa"))
    entity3.update({"embedding_field": Vector([11.0, 1.0, 2.0]), "color": "red"})
    entity4 = datastore.Entity(db.key("coffee-beans", "Liberica"))
    entity4.update({"embedding_field": Vector([3.0, 1.0, 2.0]), "color": "green"})

    db.put_multi([entity1, entity2, entity3, entity4])


def test_vector_search_basic():
    db = datastore.Client()
    add_coffee_beans_data(db)

    vector_query = vector_search_basic(db)
    results = list(vector_query.fetch())

    assert len(results) == 4
    assert results[0].name == "Liberica"
    assert results[1].name == "Robusta"
    assert results[2].name == "Arabica"
    assert results[3].name == "Excelsa"


def test_vector_search_prefilter():
    db = datastore.Client()
    add_coffee_beans_data(db)

    vector_query = vector_search_prefilter(db)
    results = list(vector_query.fetch())

    assert len(results) == 2
    assert results[0].name == "Arabica"
    assert results[1].name == "Excelsa"


def test_vector_search_distance_result_field():
    db = datastore.Client()
    add_coffee_beans_data(db)

    vector_query = vector_search_distance_result_field(db)
    results = list(vector_query.fetch())

    assert len(results) == 4
    assert results[0].name == "Liberica"
    assert results[0]["vector_distance"] == 0.0
    assert results[1].name == "Robusta"
    assert results[1]["vector_distance"] == 1.0
    assert results[2].name == "Arabica"
    assert results[2]["vector_distance"] == 7.0
    assert results[3].name == "Excelsa"
    assert results[3]["vector_distance"] == 8.0


def test_vector_search_distance_threshold():
    db = datastore.Client()
    add_coffee_beans_data(db)

    vector_query = vector_search_distance_threshold(db)
    results = list(vector_query.fetch())

    assert len(results) == 2
    assert results[0].name == "Liberica"
    assert results[1].name == "Robusta"
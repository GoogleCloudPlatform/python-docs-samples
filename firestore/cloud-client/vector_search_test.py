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

from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector

from vector_search import store_vectors
from vector_search import vector_search_basic
from vector_search import vector_search_distance_result_field
from vector_search import vector_search_distance_result_field_with_mask
from vector_search import vector_search_distance_threshold
from vector_search import vector_search_prefilter


os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_store_vectors():
    db = firestore.Client()
    store_vectors()

    results = db.collection("coffee-beans").limit(5).stream()
    results_list = list(results)
    assert len(results_list) == 1


def add_coffee_beans_data(db):
    coll = db.collection("coffee-beans")
    coll.document("bean1").set(
        {"name": "Arabica", "embedding_field": Vector([0.80522226, 0.18332680, 0.24160706]), "color": "red"}
    )
    coll.document("bean2").set(
        {"name": "Robusta", "embedding_field": Vector([0.43979567, 0.18332680, 0.24160706]), "color": "blue"}
    )
    coll.document("bean3").set(
        {"name": "Excelsa", "embedding_field": Vector([0.90477061, 0.18332680, 0.24160706]), "color": "red"}
    )
    coll.document("bean4").set(
        {
            "name": "Liberica",
            "embedding_field":  Vector([0.3416704, 0.18332680, 0.24160706]),
            "color": "green",
        }
    )


def test_vector_search_basic():
    db = firestore.Client(
        add_unique_string=False
    )  # Flag for testing purposes, needs index to be precreated
    add_coffee_beans_data(db)

    vector_query = vector_search_basic(db)
    results = list(vector_query.stream())

    assert len(results) == 4
    assert results[0].to_dict()["name"] == "Liberica"
    assert results[1].to_dict()["name"] == "Robusta"
    assert results[2].to_dict()["name"] == "Arabica"
    assert results[3].to_dict()["name"] == "Excelsa"


def test_vector_search_prefilter():
    db = firestore.Client(
        add_unique_string=False
    )  # Flag for testing purposes, needs index to be precreated
    add_coffee_beans_data(db)

    vector_query = vector_search_prefilter(db)
    results = list(vector_query.stream())

    assert len(results) == 2
    assert results[0].to_dict()["name"] == "Arabica"
    assert results[1].to_dict()["name"] == "Excelsa"


def test_vector_search_distance_result_field():
    db = firestore.Client(
        add_unique_string=False
    )  # Flag for testing purposes, needs index to be precreated
    add_coffee_beans_data(db)

    vector_query = vector_search_distance_result_field(db)
    results = list(vector_query.stream())

    assert len(results) == 4
    assert results[0].to_dict()["name"] == "Liberica"
    assert results[0].to_dict()["vector_distance"] == 0.0
    assert results[1].to_dict()["name"] == "Robusta"
    assert results[1].to_dict()["vector_distance"] == 0.09812527000000004
    assert results[2].to_dict()["name"] == "Arabica"
    assert results[2].to_dict()["vector_distance"] == 0.46355186
    assert results[3].to_dict()["name"] == "Excelsa"
    assert results[3].to_dict()["vector_distance"] == 0.56310021


def test_vector_search_distance_result_field_with_mask():
    db = firestore.Client(
        add_unique_string=False
    )  # Flag for testing purposes, needs index to be precreated
    add_coffee_beans_data(db)

    vector_query = vector_search_distance_result_field_with_mask(db)
    results = list(vector_query.stream())

    assert len(results) == 4
    assert results[0].to_dict() == {"color": "green", "vector_distance": 0.0}
    assert results[1].to_dict() == {"color": "blue", "vector_distance": 0.09812527000000004}
    assert results[2].to_dict() == {"color": "red", "vector_distance": 0.46355186}
    assert results[3].to_dict() == {"color": "red", "vector_distance": 0.56310021}


def test_vector_search_distance_threshold():
    db = firestore.Client(
        add_unique_string=False
    )  # Flag for testing purposes, needs index to be precreated
    add_coffee_beans_data(db)

    vector_query = vector_search_distance_threshold(db)
    results = list(vector_query.stream())

    assert len(results) == 4
    assert results[0].to_dict()["name"] == "Liberica"
    assert results[1].to_dict()["name"] == "Robusta"
    assert results[2].to_dict()["name"] == "Arabica"
    assert results[3].to_dict()["name"] == "Excelsa"

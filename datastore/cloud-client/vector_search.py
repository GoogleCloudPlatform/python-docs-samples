# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

def store_vectors():
    # [START datastore_store_vectors]
    from google.cloud import datastore
    from google.cloud.datastore.vector import Vector

    client = datastore.Client()

    key = client.key("coffee-beans")
    entity = datastore.Entity(key=key)
    entity.update(
        {
            "name": "Kahawa coffee beans",
            "description": "Information about the Kahawa coffee beans.",
            "embedding_field": Vector([0.18332680, 0.24160706, 0.3416704]),
        }
    )

    client.put(entity)
    # [END datastore_store_vectors]
    return client, entity


def vector_search_basic(db):
    # [START datastore_vector_search_basic]
    from google.cloud.datastore.vector import DistanceMeasure
    from google.cloud.datastore.vector import Vector
    from google.cloud.datastore.vector import FindNearest

    vector_query = db.query(
        kind="coffee-beans",
        find_nearest=FindNearest(
            vector_property="embedding_field",
            query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=5,
        )
    )
    # [END datastore_vector_search_basic]
    return vector_query


def vector_search_prefilter(db):
    # [START datastore_vector_search_prefilter]
    from google.cloud.datastore.vector import DistanceMeasure
    from google.cloud.datastore.vector import Vector
    from google.cloud.datastore.vector import FindNearest
    from google.cloud.datastore.query import PropertyFilter

    vector_query = db.query(
        kind="coffee-beans",
        filters=[PropertyFilter("color", "=", "red")],
        find_nearest=FindNearest(
            vector_property="embedding_field",
            query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=5,
        )
    )
    # [END datastore_vector_search_prefilter]
    return vector_query


def vector_search_distance_result_property(db):
    # [START datastore_vector_search_distance_result_property]
    from google.cloud.datastore.vector import DistanceMeasure
    from google.cloud.datastore.vector import Vector
    from google.cloud.datastore.vector import FindNearest

    vector_query = db.query(
        kind="coffee-beans",
        find_nearest=FindNearest(
            vector_property="embedding_field",
            query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=5,
            distance_result_property="vector_distance",
        )
    )

    for entity in vector_query.fetch():
        print(f"{entity.id}, Distance: {entity['vector_distance']}")
    # [END datastore_vector_search_distance_result_property]
    return vector_query

def vector_search_distance_result_property_projection(db):
    # [START datastore_vector_search_distance_result_property_projection]
    from google.cloud.datastore.vector import DistanceMeasure
    from google.cloud.datastore.vector import Vector
    from google.cloud.datastore.vector import FindNearest

    vector_query = db.query(
        kind="coffee-beans",
        find_nearest=FindNearest(
            vector_property="embedding_field",
            query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=5,
            distance_result_property="vector_distance",
        )
    )
    vector_query.projection = ["color"]

    for entity in vector_query.fetch():
        print(f"{entity.id}, Distance: {entity['vector_distance']}")
    # [END datastore_vector_search_distance_result_property_projection]
    return vector_query


def vector_search_distance_threshold(db):
    # [START datastore_vector_search_distance_threshold]
    from google.cloud.datastore.vector import DistanceMeasure
    from google.cloud.datastore.vector import Vector
    from google.cloud.datastore.vector import FindNearest

    vector_query = db.query(
        kind="coffee-beans",
        find_nearest=FindNearest(
            vector_property="embedding_field",
            query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=10,
            distance_threshold=0.4
        )
    )

    for entity in vector_query.fetch():
        print(f"{entity.id}")
    # [END datastore_vector_search_distance_threshold]
    return vector_query


def vector_search_large_response(db):
    # [START datastore_vector_search_large_response]
    from google.cloud.datastore.vector import DistanceMeasure
    from google.cloud.datastore.vector import Vector
    from google.cloud.datastore.vector import FindNearest

    # first, perform a vector search query retrieving just the keys
    vector_query = db.query(
        kind="coffee-beans",
        find_nearest=FindNearest(
            vector_property="embedding_field",
            query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=100,
            distance_result_property="vector_distance",
        )
    )
    vector_query.keys_only()
    vector_results = list(vector_query.fetch())
    key_list = [entity.key for entity in vector_results]
    # next, perfrom a second query for the remaining data
    full_results = db.get_multi(key_list)
    # combine and print results
    vector_map = {entity.key: entity for entity in vector_results}
    full_map = {entity.key: entity for entity in full_results}
    for key in key_list:
        print(f"distance: {vector_map[key]['vector_distance']} entity: {full_map[key]}")
    # [END datastore_vector_search_large_response]
    return key_list, vector_results, full_results
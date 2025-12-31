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
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector


def store_vectors():
    # [START firestore_store_vectors]
    from google.cloud import firestore
    from google.cloud.firestore_v1.vector import Vector

    firestore_client = firestore.Client()
    collection = firestore_client.collection("coffee-beans")
    doc = {
        "name": "Kahawa coffee beans",
        "description": "Information about the Kahawa coffee beans.",
        "embedding_field": Vector([0.18332680, 0.24160706, 0.3416704]),
    }

    collection.add(doc)
    # [END firestore_store_vectors]


def vector_search_basic(db):
    # [START firestore_vector_search_basic]
    from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
    from google.cloud.firestore_v1.vector import Vector

    collection = db.collection("coffee-beans")

    # Requires a single-field vector index
    vector_query = collection.find_nearest(
        vector_field="embedding_field",
        query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
        distance_measure=DistanceMeasure.EUCLIDEAN,
        limit=5,
    )
    # [END firestore_vector_search_basic]
    return vector_query


def vector_search_prefilter(db):
    # [START firestore_vector_search_prefilter]
    from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
    from google.cloud.firestore_v1.vector import Vector

    collection = db.collection("coffee-beans")

    # Similarity search with pre-filter
    # Requires a composite vector index
    vector_query = collection.where("color", "==", "red").find_nearest(
        vector_field="embedding_field",
        query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
        distance_measure=DistanceMeasure.EUCLIDEAN,
        limit=5,
    )
    # [END firestore_vector_search_prefilter]
    return vector_query


def vector_search_distance_result_field(db):
    # [START firestore_vector_search_distance_result_field]
    from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
    from google.cloud.firestore_v1.vector import Vector

    collection = db.collection("coffee-beans")

    vector_query = collection.find_nearest(
        vector_field="embedding_field",
        query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
        distance_measure=DistanceMeasure.EUCLIDEAN,
        limit=10,
        distance_result_field="vector_distance",
    )

    docs = vector_query.stream()

    for doc in docs:
        print(f"{doc.id}, Distance: {doc.get('vector_distance')}")
    # [END firestore_vector_search_distance_result_field]
    return vector_query


def vector_search_distance_result_field_with_mask(db):
    collection = db.collection("coffee-beans")

    # [START firestore_vector_search_distance_result_field_masked]
    vector_query = collection.select(["color", "vector_distance"]).find_nearest(
        vector_field="embedding_field",
        query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
        distance_measure=DistanceMeasure.EUCLIDEAN,
        limit=10,
        distance_result_field="vector_distance",
    )
    # [END firestore_vector_search_distance_result_field_masked]
    return vector_query


def vector_search_distance_threshold(db):
    # [START firestore_vector_search_distance_threshold]
    from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
    from google.cloud.firestore_v1.vector import Vector

    collection = db.collection("coffee-beans")

    vector_query = collection.find_nearest(
        vector_field="embedding_field",
        query_vector=Vector([0.3416704, 0.18332680, 0.24160706]),
        distance_measure=DistanceMeasure.EUCLIDEAN,
        limit=10,
        distance_threshold=4.5,
    )

    docs = vector_query.stream()

    for doc in docs:
        print(f"{doc.id}")
    # [END firestore_vector_search_distance_threshold]
    return vector_query

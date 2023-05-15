# Copyright 2019 Google LLC
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

# [START firestore_solution_sharded_counter_custom_type_async]
import random

from google.cloud import firestore


class Shard:
    """
    A shard is a distributed counter. Each shard can support being incremented
    once per second. Multiple shards are needed within a Counter to allow
    more frequent incrementing.
    """

    def __init__(self):
        self._count = 0

    def to_dict(self):
        return {"count": self._count}


class Counter:
    """
    A counter stores a collection of shards which are
    summed to return a total count. This allows for more
    frequent incrementing than a single document.
    """

    def __init__(self, num_shards):
        self._num_shards = num_shards

    # [END firestore_solution_sharded_counter_custom_type_async]

    # [START firestore_solution_sharded_counter_create_async]
    async def init_counter(self, doc_ref):
        """
        Create a given number of shards as
        subcollection of specified document.
        """
        col_ref = doc_ref.collection("shards")

        # Initialize each shard with count=0
        for num in range(self._num_shards):
            shard = Shard()
            await col_ref.document(str(num)).set(shard.to_dict())

    # [END firestore_solution_sharded_counter_create_async]

    # [START firestore_solution_sharded_counter_increment_async]
    async def increment_counter(self, doc_ref):
        """Increment a randomly picked shard."""
        doc_id = random.randint(0, self._num_shards - 1)

        shard_ref = doc_ref.collection("shards").document(str(doc_id))
        return await shard_ref.update({"count": firestore.Increment(1)})

    # [END firestore_solution_sharded_counter_increment_async]

    # [START firestore_solution_sharded_counter_get_async]
    async def get_count(self, doc_ref):
        """Return a total count across all shards."""
        total = 0
        shards = doc_ref.collection("shards").list_documents()
        async for shard in shards:
            total += (await shard.get()).to_dict().get("count", 0)
        return total

    # [END firestore_solution_sharded_counter_get_async]

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

from google.cloud import firestore
import pytest

import distributed_counters


shards_list = []
doc_ref = None


@pytest.fixture
def fs_client():
    yield firestore.Client()

    # clean up
    for shard in shards_list:
        shard.delete()

    if doc_ref:
        doc_ref.delete()


def test_distributed_counters(fs_client):
    col = fs_client.collection("dc_samples")
    doc_ref = col.document("distributed_counter")
    counter = distributed_counters.Counter(2)
    counter.init_counter(doc_ref)

    shards = doc_ref.collection("shards").list_documents()
    shards_list = [shard for shard in shards]
    assert len(shards_list) == 2

    counter.increment_counter(doc_ref)
    counter.increment_counter(doc_ref)
    assert counter.get_count(doc_ref) == 2


def test_distributed_counters_cleanup(fs_client):
    col = fs_client.collection("dc_samples")
    doc_ref = col.document("distributed_counter")

    shards = doc_ref.collection("shards").list_documents()
    shards_list = [shard for shard in shards]
    for shard in shards_list:
        shard.delete()

    doc_ref.delete()

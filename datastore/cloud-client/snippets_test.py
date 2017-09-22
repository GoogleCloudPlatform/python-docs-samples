# Copyright 2015, Google, Inc.
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

import os

from gcp_devrel.testing import eventually_consistent
from gcp_devrel.testing.flaky import flaky
from google.cloud import datastore
import pytest

import snippets

PROJECT = os.environ['GCLOUD_PROJECT']


class CleanupClient(datastore.Client):
    def __init__(self, *args, **kwargs):
        super(CleanupClient, self).__init__(*args, **kwargs)
        self.entities_to_delete = []
        self.keys_to_delete = []

    def cleanup(self):
        with self.batch():
            self.delete_multi(
                list(set([x.key for x in self.entities_to_delete])) +
                list(set(self.keys_to_delete)))


@pytest.yield_fixture
def client():
    client = CleanupClient(PROJECT)
    yield client
    client.cleanup()


@flaky
class TestDatastoreSnippets:
    # These tests mostly just test the absence of exceptions.
    def test_incomplete_key(self, client):
        assert snippets.incomplete_key(client)

    def test_named_key(self, client):
        assert snippets.named_key(client)

    def test_key_with_parent(self, client):
        assert snippets.key_with_parent(client)

    def test_key_with_multilevel_parent(self, client):
        assert snippets.key_with_multilevel_parent(client)

    def test_basic_entity(self, client):
        assert snippets.basic_entity(client)

    def test_entity_with_parent(self, client):
        assert snippets.entity_with_parent(client)

    def test_properties(self, client):
        assert snippets.properties(client)

    def test_array_value(self, client):
        assert snippets.array_value(client)

    def test_upsert(self, client):
        task = snippets.upsert(client)
        client.entities_to_delete.append(task)
        assert task

    def test_insert(self, client):
        task = snippets.insert(client)
        client.entities_to_delete.append(task)
        assert task

    def test_update(self, client):
        task = snippets.insert(client)
        client.entities_to_delete.append(task)
        assert task

    def test_lookup(self, client):
        task = snippets.lookup(client)
        client.entities_to_delete.append(task)
        assert task

    def test_delete(self, client):
        snippets.delete(client)

    def test_batch_upsert(self, client):
        tasks = snippets.batch_upsert(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    def test_batch_lookup(self, client):
        tasks = snippets.batch_lookup(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    def test_batch_delete(self, client):
        snippets.batch_delete(client)

    @eventually_consistent.mark
    def test_unindexed_property_query(self, client):
        tasks = snippets.unindexed_property_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_basic_query(self, client):
        tasks = snippets.basic_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_projection_query(self, client):
        priorities, percents = snippets.projection_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert priorities
        assert percents

    def test_ancestor_query(self, client):
        tasks = snippets.ancestor_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    def test_run_query(self, client):
        snippets.run_query(client)

    def test_cursor_paging(self, client):
        for n in range(6):
            client.entities_to_delete.append(
                snippets.insert(client))

        @eventually_consistent.call
        def _():
            results = snippets.cursor_paging(client)
            page_one, cursor_one, page_two, cursor_two = results

            assert len(page_one) == 5
            assert len(page_two)
            assert cursor_one
            assert cursor_two

    @eventually_consistent.mark
    def test_property_filter(self, client):
        tasks = snippets.property_filter(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_composite_filter(self, client):
        tasks = snippets.composite_filter(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_key_filter(self, client):
        tasks = snippets.key_filter(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_ascending_sort(self, client):
        tasks = snippets.ascending_sort(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_descending_sort(self, client):
        tasks = snippets.descending_sort(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_multi_sort(self, client):
        tasks = snippets.multi_sort(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_keys_only_query(self, client):
        keys = snippets.keys_only_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert keys

    @eventually_consistent.mark
    def test_distinct_query(self, client):
        tasks = snippets.distinct_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    def test_distinct_on_query(self, client):
        tasks = snippets.distinct_on_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    def test_kindless_query(self, client):
        tasks = snippets.kindless_query(client)
        assert tasks

    def test_inequality_range(self, client):
        snippets.inequality_range(client)

    def test_inequality_invalid(self, client):
        snippets.inequality_invalid(client)

    def test_equal_and_inequality_range(self, client):
        snippets.equal_and_inequality_range(client)

    def test_inequality_sort(self, client):
        snippets.inequality_sort(client)

    def test_inequality_sort_invalid_not_same(self, client):
        snippets.inequality_sort_invalid_not_same(client)

    def test_inequality_sort_invalid_not_first(self, client):
        snippets.inequality_sort_invalid_not_first(client)

    def test_array_value_inequality_range(self, client):
        snippets.array_value_inequality_range(client)

    def test_array_value_equality(self, client):
        snippets.array_value_equality(client)

    def test_exploding_properties(self, client):
        task = snippets.exploding_properties(client)
        assert task

    def test_transactional_update(self, client):
        keys = snippets.transactional_update(client)
        client.keys_to_delete.extend(keys)

    def test_transactional_get_or_create(self, client):
        task = snippets.transactional_get_or_create(client)
        client.entities_to_delete.append(task)
        assert task

    def transactional_single_entity_group_read_only(self, client):
        task_list, tasks_in_list = \
            snippets.transactional_single_entity_group_read_only(client)
        client.entities_to_delete.append(task_list)
        client.entities_to_delete.extend(tasks_in_list)
        assert task_list
        assert tasks_in_list

    @eventually_consistent.mark
    def test_namespace_run_query(self, client):
        all_namespaces, filtered_namespaces = snippets.namespace_run_query(
            client)
        assert all_namespaces
        assert filtered_namespaces
        assert 'google' in filtered_namespaces

    @eventually_consistent.mark
    def test_kind_run_query(self, client):
        kinds = snippets.kind_run_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert kinds
        assert 'Task' in kinds

    @eventually_consistent.mark
    def test_property_run_query(self, client):
        kinds = snippets.property_run_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert kinds
        assert 'Task' in kinds

    @eventually_consistent.mark
    def test_property_by_kind_run_query(self, client):
        reprs = snippets.property_by_kind_run_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert reprs

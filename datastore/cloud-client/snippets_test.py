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
    @staticmethod
    def test_incomplete_key(client):
        assert snippets.incomplete_key(client)

    @staticmethod
    def test_named_key(client):
        assert snippets.named_key(client)

    @staticmethod
    def test_key_with_parent(client):
        assert snippets.key_with_parent(client)

    @staticmethod
    def test_key_with_multilevel_parent(client):
        assert snippets.key_with_multilevel_parent(client)

    @staticmethod
    def test_basic_entity(client):
        assert snippets.basic_entity(client)

    @staticmethod
    def test_entity_with_parent(client):
        assert snippets.entity_with_parent(client)

    @staticmethod
    def test_properties(client):
        assert snippets.properties(client)

    @staticmethod
    def test_array_value(client):
        assert snippets.array_value(client)

    @staticmethod
    def test_upsert(client):
        task = snippets.upsert(client)
        client.entities_to_delete.append(task)
        assert task

    @staticmethod
    def test_insert(client):
        task = snippets.insert(client)
        client.entities_to_delete.append(task)
        assert task

    @staticmethod
    def test_update(client):
        task = snippets.insert(client)
        client.entities_to_delete.append(task)
        assert task

    @staticmethod
    def test_lookup(client):
        task = snippets.lookup(client)
        client.entities_to_delete.append(task)
        assert task

    @staticmethod
    def test_delete(client):
        snippets.delete(client)

    @staticmethod
    def test_batch_upsert(client):
        tasks = snippets.batch_upsert(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @staticmethod
    def test_batch_lookup(client):
        tasks = snippets.batch_lookup(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @staticmethod
    def test_batch_delete(client):
        snippets.batch_delete(client)

    @eventually_consistent.mark
    @staticmethod
    def test_unindexed_property_query(client):
        tasks = snippets.unindexed_property_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_basic_query(client):
        tasks = snippets.basic_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_projection_query(client):
        priorities, percents = snippets.projection_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert priorities
        assert percents

    @staticmethod
    def test_ancestor_query(client):
        tasks = snippets.ancestor_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @staticmethod
    def test_run_query(client):
        snippets.run_query(client)

    @staticmethod
    def test_cursor_paging(client):
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

    @eventually_consistent.mark
    @staticmethod
    def test_property_filter(client):
        tasks = snippets.property_filter(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_composite_filter(client):
        tasks = snippets.composite_filter(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_key_filter(client):
        tasks = snippets.key_filter(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_ascending_sort(client):
        tasks = snippets.ascending_sort(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_descending_sort(client):
        tasks = snippets.descending_sort(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_multi_sort(client):
        tasks = snippets.multi_sort(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @eventually_consistent.mark
    @staticmethod
    def test_keys_only_query(client):
        keys = snippets.keys_only_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert keys

    @eventually_consistent.mark
    @staticmethod
    def test_distinct_on_query(client):
        tasks = snippets.distinct_on_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks

    @staticmethod
    def test_kindless_query(client):
        tasks = snippets.kindless_query(client)
        assert tasks

    @staticmethod
    def test_inequality_range(client):
        snippets.inequality_range(client)

    @staticmethod
    def test_inequality_invalid(client):
        snippets.inequality_invalid(client)

    @staticmethod
    def test_equal_and_inequality_range(client):
        snippets.equal_and_inequality_range(client)

    @staticmethod
    def test_inequality_sort(client):
        snippets.inequality_sort(client)

    @staticmethod
    def test_inequality_sort_invalid_not_same(client):
        snippets.inequality_sort_invalid_not_same(client)

    @staticmethod
    def test_inequality_sort_invalid_not_first(client):
        snippets.inequality_sort_invalid_not_first(client)

    @staticmethod
    def test_array_value_inequality_range(client):
        snippets.array_value_inequality_range(client)

    @staticmethod
    def test_array_value_equality(client):
        snippets.array_value_equality(client)

    @staticmethod
    def test_exploding_properties(client):
        task = snippets.exploding_properties(client)
        assert task

    @staticmethod
    def test_transactional_update(client):
        keys = snippets.transactional_update(client)
        client.keys_to_delete.extend(keys)

    @staticmethod
    def test_transactional_get_or_create(client):
        task = snippets.transactional_get_or_create(client)
        client.entities_to_delete.append(task)
        assert task

    @staticmethod
    def transactional_single_entity_group_read_only(client):
        task_list, tasks_in_list = \
            snippets.transactional_single_entity_group_read_only(client)
        client.entities_to_delete.append(task_list)
        client.entities_to_delete.extend(tasks_in_list)
        assert task_list
        assert tasks_in_list

    @eventually_consistent.mark
    @staticmethod
    def test_namespace_run_query(client):
        all_namespaces, filtered_namespaces = snippets.namespace_run_query(
            client)
        assert all_namespaces
        assert filtered_namespaces
        assert 'google' in filtered_namespaces

    @eventually_consistent.mark
    @staticmethod
    def test_kind_run_query(client):
        kinds = snippets.kind_run_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert kinds
        assert 'Task' in kinds

    @eventually_consistent.mark
    @staticmethod
    def test_property_run_query(client):
        kinds = snippets.property_run_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert kinds
        assert 'Task' in kinds

    @eventually_consistent.mark
    @staticmethod
    def test_property_by_kind_run_query(client):
        reprs = snippets.property_by_kind_run_query(client)
        client.entities_to_delete.extend(
            client.query(kind='Task').fetch())
        assert reprs

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
#
from functools import wraps
import time

from gcloud import datastore
from testing import CloudTest, mark_flaky

from . import snippets


def eventually_consistent(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        # This is pretty hacky, but make datastore wait 1s after any
        # put operation to in order to account for eventual consistency.
        original_put_multi = self.client.put_multi

        def put_multi(*args, **kwargs):
            result = original_put_multi(*args, **kwargs)
            time.sleep(1)
            return result

        self.client.put_multi = put_multi

        try:
            result = f(self, *args, **kwargs)
        finally:
            self.client.put_multi = original_put_multi

        return result
    return inner


@mark_flaky
class DatastoreSnippetsTest(CloudTest):

    def setUp(self):
        super(DatastoreSnippetsTest, self).setUp()
        self.client = datastore.Client(self.config.GCLOUD_PROJECT)
        self.to_delete_entities = []
        self.to_delete_keys = []

    def tearDown(self):
        super(DatastoreSnippetsTest, self).tearDown()
        with self.client.batch():
            self.client.delete_multi(
                [x.key for x in self.to_delete_entities] + self.to_delete_keys)

    # These tests mostly just test the absence of exceptions.

    def test_incomplete_key(self):
        self.assertTrue(
            snippets.incomplete_key(self.client))

    def test_named_key(self):
        self.assertTrue(
            snippets.named_key(self.client))

    def test_key_with_parent(self):
        self.assertTrue(
            snippets.key_with_parent(self.client))

    def test_key_with_multilevel_parent(self):
        self.assertTrue(
            snippets.key_with_multilevel_parent(self.client))

    def test_basic_entity(self):
        self.assertTrue(
            snippets.basic_entity(self.client))

    def test_entity_with_parent(self):
        self.assertTrue(
            snippets.entity_with_parent(self.client))

    def test_properties(self):
        self.assertTrue(
            snippets.properties(self.client))

    def test_array_value(self):
        self.assertTrue(
            snippets.array_value(self.client))

    def test_upsert(self):
        task = snippets.upsert(self.client)
        self.to_delete_entities.append(task)
        self.assertTrue(task)

    def test_insert(self):
        task = snippets.insert(self.client)
        self.to_delete_entities.append(task)
        self.assertTrue(task)

    def test_update(self):
        task = snippets.insert(self.client)
        self.to_delete_entities.append(task)
        self.assertTrue(task)

    def test_lookup(self):
        task = snippets.lookup(self.client)
        self.to_delete_entities.append(task)
        self.assertTrue(task)

    def test_delete(self):
        snippets.delete(self.client)

    def test_batch_upsert(self):
        tasks = snippets.batch_upsert(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    def test_batch_lookup(self):
        tasks = snippets.batch_lookup(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    def test_batch_delete(self):
        snippets.batch_delete(self.client)

    @eventually_consistent
    def test_unindexed_property_query(self):
        tasks = snippets.unindexed_property_query(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_basic_query(self):
        tasks = snippets.basic_query(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_projection_query(self):
        priorities, percents = snippets.projection_query(self.client)
        self.to_delete_entities.extend(self.client.query(kind='Task').fetch())
        self.assertTrue(priorities)
        self.assertTrue(percents)

    def test_ancestor_query(self):
        tasks = snippets.ancestor_query(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_run_query(self):
        snippets.run_query(self.client)

    @eventually_consistent
    def test_cursor_paging(self):
        for n in range(6):
            self.to_delete_entities.append(
                snippets.insert(self.client))

        page_one, cursor_one, page_two, cursor_two = snippets.cursor_paging(
            self.client)

        self.assertTrue(len(page_one) == 5)
        self.assertTrue(len(page_two) == 1)
        self.assertTrue(cursor_one)
        self.assertTrue(cursor_two)

    @eventually_consistent
    def test_property_filter(self):
        tasks = snippets.property_filter(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_composite_filter(self):
        tasks = snippets.composite_filter(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_key_filter(self):
        tasks = snippets.key_filter(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_ascending_sort(self):
        tasks = snippets.ascending_sort(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_descending_sort(self):
        tasks = snippets.descending_sort(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_multi_sort(self):
        tasks = snippets.multi_sort(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_keys_only_query(self):
        keys = snippets.keys_only_query(self.client)
        self.to_delete_entities.extend(self.client.query(kind='Task').fetch())
        self.assertTrue(keys)

    @eventually_consistent
    def test_distinct_query(self):
        tasks = snippets.distinct_query(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    @eventually_consistent
    def test_distinct_on_query(self):
        tasks = snippets.distinct_on_query(self.client)
        self.to_delete_entities.extend(tasks)
        self.assertTrue(tasks)

    def test_kindless_query(self):
        tasks = snippets.kindless_query(self.client)
        self.assertTrue(tasks)

    def test_inequality_range(self):
        snippets.inequality_range(self.client)

    def test_inequality_invalid(self):
        snippets.inequality_invalid(self.client)

    def test_equal_and_inequality_range(self):
        snippets.equal_and_inequality_range(self.client)

    def test_inequality_sort(self):
        snippets.inequality_sort(self.client)

    def test_inequality_sort_invalid_not_same(self):
        snippets.inequality_sort_invalid_not_same(self.client)

    def test_inequality_sort_invalid_not_first(self):
        snippets.inequality_sort_invalid_not_first(self.client)

    def test_array_value_inequality_range(self):
        snippets.array_value_inequality_range(self.client)

    def test_array_value_equality(self):
        snippets.array_value_equality(self.client)

    def test_exploding_properties(self):
        task = snippets.exploding_properties(self.client)
        self.assertTrue(task)

    def test_transactional_update(self):
        keys = snippets.transactional_update(self.client)
        self.to_delete_keys.extend(keys)

    def test_transactional_get_or_create(self):
        task = snippets.transactional_get_or_create(self.client)
        self.to_delete_entities.append(task)
        self.assertTrue(task)

    def transactional_single_entity_group_read_only(self):
        task_list, tasks_in_list = \
            snippets.transactional_single_entity_group_read_only(self.client)
        self.to_delete_entities.append(task_list)
        self.to_delete_entities.extend(tasks_in_list)
        self.assertTrue(task_list)
        self.assertTrue(tasks_in_list)

    @eventually_consistent
    def test_namespace_run_query(self):
        all_namespaces, filtered_namespaces = snippets.namespace_run_query(
            self.client)
        self.assertTrue(all_namespaces)
        self.assertTrue(filtered_namespaces)
        self.assertTrue('google' in filtered_namespaces)

    @eventually_consistent
    def test_kind_run_query(self):
        kinds = snippets.kind_run_query(self.client)
        self.to_delete_entities.extend(self.client.query(kind='Task').fetch())
        self.assertTrue(kinds)
        self.assertTrue('Task' in kinds)

    @eventually_consistent
    def test_property_run_query(self):
        kinds = snippets.property_run_query(self.client)
        self.to_delete_entities.extend(self.client.query(kind='Task').fetch())
        self.assertTrue(kinds)
        self.assertTrue('Task' in kinds)

    @eventually_consistent
    def test_property_by_kind_run_query(self):
        reprs = snippets.property_by_kind_run_query(self.client)
        self.to_delete_entities.extend(self.client.query(kind='Task').fetch())
        self.assertTrue(reprs)

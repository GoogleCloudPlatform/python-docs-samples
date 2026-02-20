# Copyright 2022 Google, Inc.
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

import backoff
import google.api_core.exceptions
from google.cloud import datastore
from google.cloud import datastore_admin_v1
import pytest

import snippets

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


class CleanupClient(datastore.Client):
    def __init__(self, *args, **kwargs):
        super(CleanupClient, self).__init__(*args, **kwargs)
        self.entities_to_delete = []
        self.keys_to_delete = []

    def cleanup(self):
        with self.batch():
            self.delete_multi(
                list(set([x.key for x in self.entities_to_delete if x]))
                + list(set(self.keys_to_delete))
            )


@pytest.fixture
def client():
    client = CleanupClient(PROJECT)
    yield client
    client.cleanup()


@pytest.fixture(scope="session", autouse=True)
def setup_indexes(request):
    # Set up required indexes
    admin_client = datastore_admin_v1.DatastoreAdminClient()

    indexes = []
    done_property_index = datastore_admin_v1.Index.IndexedProperty(
        name="done", direction=datastore_admin_v1.Index.Direction.ASCENDING
    )
    hour_property_index = datastore_admin_v1.Index.IndexedProperty(
        name="hours", direction=datastore_admin_v1.Index.Direction.ASCENDING
    )
    done_hour_index = datastore_admin_v1.Index(
        kind="Task",
        ancestor=datastore_admin_v1.Index.AncestorMode.NONE,
        properties=[done_property_index, hour_property_index],
    )
    indexes.append(done_hour_index)

    for index in indexes:
        request = datastore_admin_v1.CreateIndexRequest(project_id=PROJECT, index=index)
        # Create the required index
        # Dependant tests will fail until the index is ready
        try:
            admin_client.create_index(request)
        # Pass if the index already exists
        except (google.api_core.exceptions.AlreadyExists):
            pass


@pytest.mark.flaky
class TestDatastoreSnippets:
    # These tests mostly just test the absence of exceptions.

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_in_query(self, client):
        tasks = snippets.in_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks is not None

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_not_equals_query(self, client):
        tasks = snippets.not_equals_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks is not None

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_not_in_query(self, client):
        tasks = snippets.not_in_query(client)
        client.entities_to_delete.extend(tasks)
        assert tasks is not None

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_query_with_readtime(self, client):
        tasks = snippets.query_with_readtime(client)
        client.entities_to_delete.extend(tasks)
        assert tasks is not None

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_count_query_in_transaction(self, client):
        with pytest.raises(ValueError) as excinfo:
            snippets.count_query_in_transaction(client)
        assert "User 'John' cannot have more than 2 tasks" in str(excinfo.value)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_count_query_on_kind(self, capsys, client):
        tasks = snippets.count_query_on_kind(client)
        captured = capsys.readouterr()
        assert (
            captured.out.strip() == "Total tasks (accessible from default alias) is 2"
        )
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_count_query_with_limit(self, capsys, client):
        tasks = snippets.count_query_with_limit(client)
        captured = capsys.readouterr()
        assert captured.out.strip() == "We have at least 2 tasks"
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_count_query_property_filter(self, capsys, client):
        tasks = snippets.count_query_property_filter(client)
        captured = capsys.readouterr()

        assert "Total completed tasks count is 2" in captured.out
        assert "Total remaining tasks count is 1" in captured.out
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_count_query_with_stale_read(self, capsys, client):
        tasks = snippets.count_query_with_stale_read(client)
        captured = capsys.readouterr()

        assert "Latest tasks count is 3" in captured.out
        assert "Stale tasks count is 2" in captured.out
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_sum_query_on_kind(self, capsys, client):
        tasks = snippets.sum_query_on_kind(client)
        captured = capsys.readouterr()
        assert captured.out.strip() == "Total sum of hours in tasks is 9"
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_sum_query_property_filter(self, capsys, client):
        tasks = snippets.sum_query_property_filter(client)
        captured = capsys.readouterr()
        assert captured.out.strip() == "Total sum of hours in completed tasks is 8"
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_avg_query_on_kind(self, capsys, client):
        tasks = snippets.avg_query_on_kind(client)
        captured = capsys.readouterr()
        assert captured.out.strip() == "Total average of hours in tasks is 3.0"
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_avg_query_property_filter(self, capsys, client):
        tasks = snippets.avg_query_property_filter(client)
        captured = capsys.readouterr()
        assert (
            captured.out.strip() == "Total average of hours in completed tasks is 4.0"
        )
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_multiple_aggregations_query(self, capsys, client):
        tasks = snippets.multiple_aggregations_query(client)
        captured = capsys.readouterr()
        assert "avg_aggregation value is 3.0" in captured.out
        assert "count_aggregation value is 3" in captured.out
        assert "sum_aggregation value is 9" in captured.out
        assert captured.err == ""

        client.entities_to_delete.extend(tasks)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_explain_analyze_entity(self, capsys, client):
        snippets.explain_analyze_entity(client)
        captured = capsys.readouterr()
        assert (
            "Indexes used: [{'properties': '(__name__ ASC)', 'query_scope': 'Collection group'}]"
            in captured.out
        )
        assert "Results returned: 0" in captured.out
        assert "Execution duration: 0:00" in captured.out
        assert "Read operations: 0" in captured.out
        assert "Debug stats: {" in captured.out
        assert captured.err == ""

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_explain_entity(self, capsys, client):
        snippets.explain_entity(client)
        captured = capsys.readouterr()
        assert (
            "Indexes used: [{'properties': '(__name__ ASC)', 'query_scope': 'Collection group'}]"
            in captured.out
        )
        assert captured.err == ""

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_explain_analyze_aggregation(self, capsys, client):
        snippets.explain_analyze_aggregation(client)
        captured = capsys.readouterr()
        assert (
            "Indexes used: [{'properties': '(__name__ ASC)', 'query_scope': 'Collection group'}]"
            in captured.out
        )
        assert "Results returned: 1" in captured.out
        assert "Execution duration: 0:00" in captured.out
        assert "Read operations: 1" in captured.out
        assert "Debug stats: {" in captured.out
        assert captured.err == ""

    @backoff.on_exception(backoff.expo, AssertionError, max_time=240)
    def test_explain_aggregation(self, capsys, client):
        snippets.explain_aggregation(client)
        captured = capsys.readouterr()
        assert (
            "Indexes used: [{'properties': '(__name__ ASC)', 'query_scope': 'Collection group'}]"
            in captured.out
        )
        assert captured.err == ""

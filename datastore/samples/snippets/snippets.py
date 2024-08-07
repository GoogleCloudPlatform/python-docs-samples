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

import argparse
from datetime import datetime, timedelta, timezone
from pprint import pprint
import time

from google.cloud import datastore  # noqa: I100


def _preamble():
    # [START datastore_size_coloration_query]
    from google.cloud import datastore

    # For help authenticating your client, visit
    # https://cloud.google.com/docs/authentication/getting-started
    client = datastore.Client()

    # [END datastore_size_coloration_query]
    assert client is not None


def in_query(client):
    # [START datastore_in_query]
    query = client.query(kind="Task")
    query.add_filter("tag", "IN", ["learn", "study"])
    # [END datastore_in_query]

    return list(query.fetch())


def not_equals_query(client):
    # [START datastore_not_equals_query]
    query = client.query(kind="Task")
    query.add_filter("category", "!=", "work")
    # [END datastore_not_equals_query]

    return list(query.fetch())


def not_in_query(client):
    # [START datastore_not_in_query]
    query = client.query(kind="Task")
    query.add_filter("category", "NOT_IN", ["work", "chores", "school"])
    # [END datastore_not_in_query]

    return list(query.fetch())


def query_with_readtime(client):
    # [START datastore_stale_read]
    # Create a read time of 15 seconds in the past
    read_time = datetime.now(timezone.utc) - timedelta(seconds=15)

    # Fetch an entity with read_time
    task_key = client.key("Task", "sampletask")
    entity = client.get(task_key, read_time=read_time)

    # Query Task entities with read_time
    query = client.query(kind="Task")
    tasks = query.fetch(read_time=read_time, limit=10)
    # [END datastore_stale_read]

    results = list(tasks)
    results.append(entity)

    return results


def count_query_in_transaction(client):
    # [START datastore_count_in_transaction]
    task1 = datastore.Entity(client.key("Task", "task1"))
    task2 = datastore.Entity(client.key("Task", "task2"))

    task1["owner"] = "john"
    task2["owner"] = "john"

    tasks = [task1, task2]
    client.put_multi(tasks)

    with client.transaction() as transaction:

        tasks_of_john = client.query(kind="Task")
        tasks_of_john.add_filter("owner", "=", "john")
        total_tasks_query = client.aggregation_query(tasks_of_john)

        query_result = total_tasks_query.count(alias="tasks_count").fetch()
        for task_result in query_result:
            tasks_count = task_result[0]
            if tasks_count.value < 2:
                task3 = datastore.Entity(client.key("Task", "task3"))
                task3["owner"] = "john"
                transaction.put(task3)
                tasks.append(task3)
            else:
                print(f"Found existing {tasks_count.value} tasks, rolling back")
                client.entities_to_delete.extend(tasks)
                raise ValueError("User 'John' cannot have more than 2 tasks")
    # [END datastore_count_in_transaction]


def count_query_on_kind(client):
    # [START datastore_count_on_kind]
    task1 = datastore.Entity(client.key("Task", "task1"))
    task2 = datastore.Entity(client.key("Task", "task2"))

    tasks = [task1, task2]
    client.put_multi(tasks)
    all_tasks_query = client.query(kind="Task")
    all_tasks_count_query = client.aggregation_query(all_tasks_query).count()
    query_result = all_tasks_count_query.fetch()
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            print(f"Total tasks (accessible from default alias) is {aggregation.value}")
    # [END datastore_count_on_kind]
    return tasks


def count_query_with_limit(client):
    # [START datastore_count_with_limit]
    task1 = datastore.Entity(client.key("Task", "task1"))
    task2 = datastore.Entity(client.key("Task", "task2"))
    task3 = datastore.Entity(client.key("Task", "task3"))

    tasks = [task1, task2, task3]
    client.put_multi(tasks)
    all_tasks_query = client.query(kind="Task")
    all_tasks_count_query = client.aggregation_query(all_tasks_query).count()
    query_result = all_tasks_count_query.fetch(limit=2)
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            print(f"We have at least {aggregation.value} tasks")
    # [END datastore_count_with_limit]
    return tasks


def count_query_property_filter(client):
    # [START datastore_count_with_property_filter]
    task1 = datastore.Entity(client.key("Task", "task1"))
    task2 = datastore.Entity(client.key("Task", "task2"))
    task3 = datastore.Entity(client.key("Task", "task3"))

    task1["done"] = True
    task2["done"] = False
    task3["done"] = True

    tasks = [task1, task2, task3]
    client.put_multi(tasks)
    completed_tasks = client.query(kind="Task").add_filter("done", "=", True)
    remaining_tasks = client.query(kind="Task").add_filter("done", "=", False)

    completed_tasks_query = client.aggregation_query(query=completed_tasks).count(
        alias="total_completed_count"
    )
    remaining_tasks_query = client.aggregation_query(query=remaining_tasks).count(
        alias="total_remaining_count"
    )

    completed_query_result = completed_tasks_query.fetch()
    for aggregation_results in completed_query_result:
        for aggregation_result in aggregation_results:
            if aggregation_result.alias == "total_completed_count":
                print(f"Total completed tasks count is {aggregation_result.value}")

    remaining_query_result = remaining_tasks_query.fetch()
    for aggregation_results in remaining_query_result:
        for aggregation_result in aggregation_results:
            if aggregation_result.alias == "total_remaining_count":
                print(f"Total remaining tasks count is {aggregation_result.value}")
    # [END datastore_count_with_property_filter]
    return tasks


def count_query_with_stale_read(client):

    tasks = [task for task in client.query(kind="Task").fetch()]
    client.delete_multi(tasks)  # ensure the database is empty before starting

    # [START datastore_count_query_with_stale_read]
    task1 = datastore.Entity(client.key("Task", "task1"))
    task2 = datastore.Entity(client.key("Task", "task2"))

    # Saving two tasks
    task1["done"] = True
    task2["done"] = False
    client.put_multi([task1, task2])
    time.sleep(10)

    past_timestamp = datetime.now(
        timezone.utc
    )  # we have two tasks in database at this time.
    time.sleep(10)

    # Saving third task
    task3 = datastore.Entity(client.key("Task", "task3"))
    task3["done"] = False
    client.put(task3)

    all_tasks = client.query(kind="Task")
    all_tasks_count = client.aggregation_query(
        query=all_tasks,
    ).count(alias="all_tasks_count")

    # Executing aggregation query
    query_result = all_tasks_count.fetch()
    for aggregation_results in query_result:
        for aggregation_result in aggregation_results:
            print(f"Latest tasks count is {aggregation_result.value}")

    # Executing aggregation query with past timestamp
    tasks_in_past = client.aggregation_query(query=all_tasks).count(
        alias="tasks_in_past"
    )
    tasks_in_the_past_query_result = tasks_in_past.fetch(read_time=past_timestamp)
    for aggregation_results in tasks_in_the_past_query_result:
        for aggregation_result in aggregation_results:
            print(f"Stale tasks count is {aggregation_result.value}")
    # [END datastore_count_query_with_stale_read]
    return [task1, task2, task3]


def sum_query_on_kind(client):
    # [START datastore_sum_aggregation_query_on_kind]
    # Set up sample entities
    # Use incomplete key to auto-generate ID
    task1 = datastore.Entity(client.key("Task"))
    task2 = datastore.Entity(client.key("Task"))
    task3 = datastore.Entity(client.key("Task"))

    task1["hours"] = 5
    task2["hours"] = 3
    task3["hours"] = 1

    tasks = [task1, task2, task3]
    client.put_multi(tasks)

    # Execute sum aggregation query
    all_tasks_query = client.query(kind="Task")
    all_tasks_sum_query = client.aggregation_query(all_tasks_query).sum("hours")
    query_result = all_tasks_sum_query.fetch()
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            print(f"Total sum of hours in tasks is {aggregation.value}")
    # [END datastore_sum_aggregation_query_on_kind]
    return tasks


def sum_query_property_filter(client):
    # [START datastore_sum_aggregation_query_with_filters]
    # Set up sample entities
    # Use incomplete key to auto-generate ID
    task1 = datastore.Entity(client.key("Task"))
    task2 = datastore.Entity(client.key("Task"))
    task3 = datastore.Entity(client.key("Task"))

    task1["hours"] = 5
    task2["hours"] = 3
    task3["hours"] = 1

    task1["done"] = True
    task2["done"] = True
    task3["done"] = False

    tasks = [task1, task2, task3]
    client.put_multi(tasks)

    # Execute sum aggregation query with filters
    completed_tasks = client.query(kind="Task").add_filter("done", "=", True)
    completed_tasks_query = client.aggregation_query(query=completed_tasks).sum(
        property_ref="hours", alias="total_completed_sum_hours"
    )

    completed_query_result = completed_tasks_query.fetch()
    for aggregation_results in completed_query_result:
        for aggregation_result in aggregation_results:
            if aggregation_result.alias == "total_completed_sum_hours":
                print(
                    f"Total sum of hours in completed tasks is {aggregation_result.value}"
                )
    # [END datastore_sum_aggregation_query_with_filters]
    return tasks


def avg_query_on_kind(client):
    # [START datastore_avg_aggregation_query_on_kind]
    # Set up sample entities
    # Use incomplete key to auto-generate ID
    task1 = datastore.Entity(client.key("Task"))
    task2 = datastore.Entity(client.key("Task"))
    task3 = datastore.Entity(client.key("Task"))

    task1["hours"] = 5
    task2["hours"] = 3
    task3["hours"] = 1

    tasks = [task1, task2, task3]
    client.put_multi(tasks)

    # Execute average aggregation query
    all_tasks_query = client.query(kind="Task")
    all_tasks_avg_query = client.aggregation_query(all_tasks_query).avg("hours")
    query_result = all_tasks_avg_query.fetch()
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            print(f"Total average of hours in tasks is {aggregation.value}")
    # [END datastore_avg_aggregation_query_on_kind]
    return tasks


def avg_query_property_filter(client):
    # [START datastore_avg_aggregation_query_with_filters]
    # Set up sample entities
    # Use incomplete key to auto-generate ID
    task1 = datastore.Entity(client.key("Task"))
    task2 = datastore.Entity(client.key("Task"))
    task3 = datastore.Entity(client.key("Task"))

    task1["hours"] = 5
    task2["hours"] = 3
    task3["hours"] = 1

    task1["done"] = True
    task2["done"] = True
    task3["done"] = False

    tasks = [task1, task2, task3]
    client.put_multi(tasks)

    # Execute average aggregation query with filters
    completed_tasks = client.query(kind="Task").add_filter("done", "=", True)
    completed_tasks_query = client.aggregation_query(query=completed_tasks).avg(
        property_ref="hours", alias="total_completed_avg_hours"
    )

    completed_query_result = completed_tasks_query.fetch()
    for aggregation_results in completed_query_result:
        for aggregation_result in aggregation_results:
            if aggregation_result.alias == "total_completed_avg_hours":
                print(
                    f"Total average of hours in completed tasks is {aggregation_result.value}"
                )
    # [END datastore_avg_aggregation_query_with_filters]
    return tasks


def multiple_aggregations_query(client):
    # [START datastore_multiple_aggregation_in_structured_query]
    # Set up sample entities
    # Use incomplete key to auto-generate ID
    task1 = datastore.Entity(client.key("Task"))
    task2 = datastore.Entity(client.key("Task"))
    task3 = datastore.Entity(client.key("Task"))

    task1["hours"] = 5
    task2["hours"] = 3
    task3["hours"] = 1

    tasks = [task1, task2, task3]
    client.put_multi(tasks)

    # Execute query with multiple aggregations
    all_tasks_query = client.query(kind="Task")
    aggregation_query = client.aggregation_query(all_tasks_query)
    # Add aggregations
    aggregation_query.add_aggregations(
        [
            datastore.aggregation.CountAggregation(alias="count_aggregation"),
            datastore.aggregation.SumAggregation(
                property_ref="hours", alias="sum_aggregation"
            ),
            datastore.aggregation.AvgAggregation(
                property_ref="hours", alias="avg_aggregation"
            ),
        ]
    )

    query_result = aggregation_query.fetch()
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            print(f"{aggregation.alias} value is {aggregation.value}")
    # [END datastore_multiple_aggregation_in_structured_query]
    return tasks


def explain_analyze_entity(client):
    # [START datastore_query_explain_analyze_entity]
    # Build the query with explain_options
    # analzye = true to get back the query stats, plan info, and query results
    query = client.query(
        kind="Task", explain_options=datastore.ExplainOptions(analyze=True)
    )

    # initiate the query
    iterator = query.fetch()

    # explain_metrics is only available after query is completed
    for task_result in iterator:
        print(task_result)

    # get the plan summary
    plan_summary = iterator.explain_metrics.plan_summary
    print(f"Indexes used: {plan_summary.indexes_used}")

    # get the execution stats
    execution_stats = iterator.explain_metrics.execution_stats
    print(f"Results returned: {execution_stats.results_returned}")
    print(f"Execution duration: {execution_stats.execution_duration}")
    print(f"Read operations: {execution_stats.read_operations}")
    print(f"Debug stats: {execution_stats.debug_stats}")
    # [END datastore_query_explain_analyze_entity]


def explain_entity(client):
    # [START datastore_query_explain_entity]
    # Build the query with explain_options
    # by default (analyze = false), only plan_summary property is available
    query = client.query(kind="Task", explain_options=datastore.ExplainOptions())

    # initiate the query
    iterator = query.fetch()

    # get the plan summary
    plan_summary = iterator.explain_metrics.plan_summary
    print(f"Indexes used: {plan_summary.indexes_used}")
    # [END datastore_query_explain_entity]


def explain_analyze_aggregation(client):
    # [START datastore_query_explain_analyze_aggregation]
    # Build the aggregation query with explain_options
    # analzye = true to get back the query stats, plan info, and query results
    all_tasks_query = client.query(kind="Task")
    count_query = client.aggregation_query(
        all_tasks_query, explain_options=datastore.ExplainOptions(analyze=True)
    ).count()

    # initiate the query
    iterator = count_query.fetch()

    # explain_metrics is only available after query is completed
    for task_result in iterator:
        print(task_result)

    # get the plan summary
    plan_summary = iterator.explain_metrics.plan_summary
    print(f"Indexes used: {plan_summary.indexes_used}")

    # get the execution stats
    execution_stats = iterator.explain_metrics.execution_stats
    print(f"Results returned: {execution_stats.results_returned}")
    print(f"Execution duration: {execution_stats.execution_duration}")
    print(f"Read operations: {execution_stats.read_operations}")
    print(f"Debug stats: {execution_stats.debug_stats}")
    # [END datastore_query_explain_analyze_aggregation]


def explain_aggregation(client):
    # [START datastore_query_explain_aggregation]
    # Build the aggregation query with explain_options
    # by default (analyze = false), only plan_summary property is available
    all_tasks_query = client.query(kind="Task")
    count_query = client.aggregation_query(
        all_tasks_query, explain_options=datastore.ExplainOptions()
    ).count()

    # initiate the query
    iterator = count_query.fetch()

    # get the plan summary
    plan_summary = iterator.explain_metrics.plan_summary
    print(f"Indexes used: {plan_summary.indexes_used}")
    # [END datastore_query_explain_aggregation]


def main(project_id):
    client = datastore.Client(project_id)

    for name, function in globals().items():
        if name in (
            "main",
            "_preamble",
            "defaultdict",
            "datetime",
            "timezone",
            "timedelta",
        ) or not callable(function):
            continue

        print(name)
        pprint(function(client))
        print("\n-----------------\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Demonstrates datastore API operations."
    )
    parser.add_argument("project_id", help="Your cloud project ID.")

    args = parser.parse_args()

    main(args.project_id)

# Copyright 2023 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Two Airflow DAGs that demonstrate the mechanism of triggering DAGs with Pub/Sub messages

    Usage: Replace <PROJECT_ID> with the project ID of your project
"""

# [START composer_pubsub_trigger_dag]
from __future__ import annotations

from datetime import datetime
import time

from airflow import DAG
from airflow import XComArg
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.google.cloud.operators.pubsub import (
    PubSubCreateSubscriptionOperator,
    PubSubPullOperator,
)

PROJECT_ID = "<PROJECT_ID>"
TOPIC_ID = "dag-topic-trigger"
SUBSCRIPTION = "trigger_dag_subscription"


def handle_messages(pulled_messages, context):
    dag_ids = list()
    for idx, m in enumerate(pulled_messages):
        data = m.message.data.decode('utf-8')
        print(f'message {idx} data is {data}')
        dag_ids.append(data)
    return dag_ids


# This DAG will run minutely and handle pub/sub messages by triggering target DAG
with DAG('trigger_dag',
         start_date=datetime(2021, 1, 1),
         schedule_interval="* * * * *",
         max_active_runs=1,
         catchup=False) as trigger_dag:

    # If subscription exists, we will use it. If not - create new one
    subscribe_task = PubSubCreateSubscriptionOperator(task_id="subscribe_task",
                                                      project_id=PROJECT_ID,
                                                      topic=TOPIC_ID,
                                                      subscription=SUBSCRIPTION)

    subscription = subscribe_task.output

    # Proceed maximum 50 messages in callback function handle_messages
    # Here we acknowledge messages automatically. You can use PubSubHook.acknowledge to acknowledge in downstream tasks
    # https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/pubsub/index.html#airflow.providers.google.cloud.hooks.pubsub.PubSubHook.acknowledge
    pull_messages_operator = PubSubPullOperator(
        task_id="pull_messages_operator",
        project_id=PROJECT_ID,
        ack_messages=True,
        messages_callback=handle_messages,
        subscription=subscription,
        max_messages=50,
    )

    # Here we use Dynamic Task Mapping to trigger DAGs according to messages content
    # https://airflow.apache.org/docs/apache-airflow/2.3.0/concepts/dynamic-task-mapping.html
    trigger_target_dag = TriggerDagRunOperator\
        .partial(task_id='trigger_target')\
        .expand(trigger_dag_id=XComArg(pull_messages_operator))

    (subscribe_task >> pull_messages_operator >> trigger_target_dag)


def _some_heavy_task():
    print('Do some operation...')
    time.sleep(1)
    print('Done!')


# Simple target DAG
with DAG(
        'target_dag',
        start_date=datetime(2022, 1, 1),
        # Not scheduled, trigger only
        schedule_interval=None,
        catchup=False) as target_dag:

    some_heavy_task = PythonOperator(task_id='some_heavy_task',
                                     python_callable=_some_heavy_task)

    (some_heavy_task)

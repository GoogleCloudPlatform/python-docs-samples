# Copyright 2023 Google LLC
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

"""Sample app that uses the Data Loss Prevent API to perform risk anaylsis."""


import argparse


# [START dlp_categorical_stats]
import concurrent.futures

import google.cloud.dlp
import google.cloud.pubsub


def categorical_risk_analysis(
    project: str,
    table_project_id: str,
    dataset_id: str,
    table_id: str,
    column_name: str,
    topic_id: str,
    subscription_id: str,
    timeout: int = 300,
) -> None:
    """Uses the Data Loss Prevention API to compute risk metrics of a column
       of categorical data in a Google BigQuery table.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_project_id: The Google Cloud project id where the BigQuery table
            is stored.
        dataset_id: The id of the dataset to inspect.
        table_id: The id of the table to inspect.
        column_name: The name of the column to compute risk metrics for.
        topic_id: The name of the Pub/Sub topic to notify once the job
            completes.
        subscription_id: The name of the Pub/Sub subscription to use when
            listening for job completion notifications.
        timeout: The number of seconds to wait for a response from the API.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into full resource ids.
    topic = google.cloud.pubsub.PublisherClient.topic_path(project, topic_id)
    parent = f"projects/{project}/locations/global"

    # Location info of the BigQuery table.
    source_table = {
        "project_id": table_project_id,
        "dataset_id": dataset_id,
        "table_id": table_id,
    }

    # Tell the API where to send a notification when the job is complete.
    actions = [{"pub_sub": {"topic": topic}}]

    # Configure risk analysis job
    # Give the name of the numeric column to compute risk metrics for
    risk_job = {
        "privacy_metric": {
            "categorical_stats_config": {"field": {"name": column_name}}
        },
        "source_table": source_table,
        "actions": actions,
    }

    # Call API to start risk analysis job
    operation = dlp.create_dlp_job(request={"parent": parent, "risk_job": risk_job})

    def callback(message: google.cloud.pubsub_v1.subscriber.message.Message) -> None:
        if message.attributes["DlpJobName"] == operation.name:
            # This is the message we're looking for, so acknowledge it.
            message.ack()

            # Now that the job is done, fetch the results and print them.
            job = dlp.get_dlp_job(request={"name": operation.name})
            print(f"Job name: {job.name}")
            histogram_buckets = (
                job.risk_details.categorical_stats_result.value_frequency_histogram_buckets  # noqa: E501
            )
            # Print bucket stats
            for i, bucket in enumerate(histogram_buckets):
                print(f"Bucket {i}:")
                print(
                    "   Most common value occurs {} time(s)".format(
                        bucket.value_frequency_upper_bound
                    )
                )
                print(
                    "   Least common value occurs {} time(s)".format(
                        bucket.value_frequency_lower_bound
                    )
                )
                print(f"   {bucket.bucket_size} unique values total.")
                for value in bucket.bucket_values:
                    print(
                        "   Value {} occurs {} time(s)".format(
                            value.value.integer_value, value.count
                        )
                    )
            subscription.set_result(None)
        else:
            # This is not the message we're looking for.
            message.drop()

    # Create a Pub/Sub client and find the subscription. The subscription is
    # expected to already be listening to the topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_id)
    subscription = subscriber.subscribe(subscription_path, callback)

    try:
        subscription.result(timeout=timeout)
    except concurrent.futures.TimeoutError:
        print(
            "No event received before the timeout. Please verify that the "
            "subscription provided is subscribed to the topic provided."
        )
        subscription.close()


# [END dlp_categorical_stats]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "table_project_id",
        help="The Google Cloud project id where the BigQuery table is stored.",
    )
    parser.add_argument("dataset_id", help="The id of the dataset to inspect.")
    parser.add_argument("table_id", help="The id of the table to inspect.")
    parser.add_argument(
        "column_name",
        help="The name of the column to compute risk metrics for.",
    )
    parser.add_argument(
        "topic_id",
        help="The name of the Pub/Sub topic to notify once the job completes.",
    )
    parser.add_argument(
        "subscription_id",
        help="The name of the Pub/Sub subscription to use when listening for"
        "job completion notifications.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="The number of seconds to wait for a response from the API.",
    )

    args = parser.parse_args()

    categorical_risk_analysis(
        args.project,
        args.table_project_id,
        args.dataset_id,
        args.table_id,
        args.column_name,
        args.topic_id,
        args.subscription_id,
        timeout=args.timeout,
    )

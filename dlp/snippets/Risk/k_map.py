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


# [START dlp_k_map]
import concurrent.futures
from typing import List

import google.cloud.dlp
from google.cloud.dlp_v2 import types
import google.cloud.pubsub


def k_map_estimate_analysis(
    project: str,
    table_project_id: str,
    dataset_id: str,
    table_id: str,
    topic_id: str,
    subscription_id: str,
    quasi_ids: List[str],
    info_types: List[str],
    region_code: str = "US",
    timeout: int = 300,
) -> None:
    """Uses the Data Loss Prevention API to compute the k-map risk estimation
        of a column set in a Google BigQuery table.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_project_id: The Google Cloud project id where the BigQuery table
            is stored.
        dataset_id: The id of the dataset to inspect.
        table_id: The id of the table to inspect.
        topic_id: The name of the Pub/Sub topic to notify once the job
            completes.
        subscription_id: The name of the Pub/Sub subscription to use when
            listening for job completion notifications.
        quasi_ids: A set of columns that form a composite key and optionally
            their re-identification distributions.
        info_types: Type of information of the quasi_id in order to provide a
            statistical model of population.
        region_code: The ISO 3166-1 region code that the data is representative
            of. Can be omitted if using a region-specific infoType (such as
            US_ZIP_5)
        timeout: The number of seconds to wait for a response from the API.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Create helper function for unpacking values
    def get_values(obj: types.Value) -> int:
        return int(obj.integer_value)

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

    # Check that numbers of quasi-ids and info types are equal
    if len(quasi_ids) != len(info_types):
        raise ValueError(
            """Number of infoTypes and number of quasi-identifiers
                            must be equal!"""
        )

    # Convert quasi id list to Protobuf type
    def map_fields(quasi_id: str, info_type: str) -> dict:
        return {"field": {"name": quasi_id}, "info_type": {"name": info_type}}

    quasi_ids = map(map_fields, quasi_ids, info_types)

    # Tell the API where to send a notification when the job is complete.
    actions = [{"pub_sub": {"topic": topic}}]

    # Configure risk analysis job
    # Give the name of the numeric column to compute risk metrics for
    risk_job = {
        "privacy_metric": {
            "k_map_estimation_config": {
                "quasi_ids": quasi_ids,
                "region_code": region_code,
            }
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
                job.risk_details.k_map_estimation_result.k_map_estimation_histogram
            )
            # Print bucket stats
            for i, bucket in enumerate(histogram_buckets):
                print(f"Bucket {i}:")
                print(
                    "   Anonymity range: [{}, {}]".format(
                        bucket.min_anonymity, bucket.max_anonymity
                    )
                )
                print(f"   Size: {bucket.bucket_size}")
                for value_bucket in bucket.bucket_values:
                    print(
                        "   Values: {}".format(
                            map(get_values, value_bucket.quasi_ids_values)
                        )
                    )
                    print(
                        "   Estimated k-map anonymity: {}".format(
                            value_bucket.estimated_anonymity
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


# [END dlp_k_map]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

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
        "topic_id",
        help="The name of the Pub/Sub topic to notify once the job completes.",
    )
    parser.add_argument(
        "subscription_id",
        help="The name of the Pub/Sub subscription to use when listening for"
        "job completion notifications.",
    )
    parser.add_argument(
        "quasi_ids",
        nargs="+",
        help="A set of columns that form a composite key.",
    )
    parser.add_argument(
        "-t",
        "--info-types",
        nargs="+",
        help="Type of information of the quasi_id in order to provide a"
        "statistical model of population.",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--region-code",
        default="US",
        help="The ISO 3166-1 region code that the data is representative of.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="The number of seconds to wait for a response from the API.",
    )

    args = parser.parse_args()
    k_map_estimate_analysis(
        args.project,
        args.table_project_id,
        args.dataset_id,
        args.table_id,
        args.topic_id,
        args.subscription_id,
        args.quasi_ids,
        args.info_types,
        region_code=args.region_code,
        timeout=args.timeout,
    )

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

"""Sample app that uses the Data Loss Prevention API to inspect a string, a
local file or a file on Google Cloud Storage."""


import argparse

# [START dlp_inspect_bigquery]
import threading
from typing import List, Optional

import google.cloud.dlp
import google.cloud.pubsub


def inspect_bigquery(
    project: str,
    bigquery_project: str,
    dataset_id: str,
    table_id: str,
    topic_id: str,
    subscription_id: str,
    info_types: List[str],
    custom_dictionaries: List[str] = None,
    custom_regexes: List[str] = None,
    min_likelihood: Optional[int] = None,
    max_findings: Optional[int] = None,
    timeout: int = 500,
) -> None:
    """Uses the Data Loss Prevention API to analyze BigQuery data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        bigquery_project: The Google Cloud project id of the target table.
        dataset_id: The id of the target BigQuery dataset.
        table_id: The id of the target BigQuery table.
        topic_id: The id of the Cloud Pub/Sub topic to which the API will
            broadcast job completion. The topic must already exist.
        subscription_id: The id of the Cloud Pub/Sub subscription to listen on
            while waiting for job completion. The subscription must already
            exist and be subscribed to the topic.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        timeout: The number of seconds to wait for a response from the API.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    if not info_types:
        info_types = ["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"]
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare custom_info_types by parsing the dictionary word lists and
    # regex patterns.
    if custom_dictionaries is None:
        custom_dictionaries = []
    dictionaries = [
        {
            "info_type": {"name": f"CUSTOM_DICTIONARY_{i}"},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": f"CUSTOM_REGEX_{i}"},
            "regex": {"pattern": custom_regex},
        }
        for i, custom_regex in enumerate(custom_regexes)
    ]
    custom_info_types = dictionaries + regexes

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "custom_info_types": custom_info_types,
        "min_likelihood": min_likelihood,
        "limits": {"max_findings_per_request": max_findings},
    }

    # Construct a storage_config containing the target Bigquery info.
    storage_config = {
        "big_query_options": {
            "table_reference": {
                "project_id": bigquery_project,
                "dataset_id": dataset_id,
                "table_id": table_id,
            }
        }
    }

    # Convert the project id into full resource ids.
    topic = google.cloud.pubsub.PublisherClient.topic_path(project, topic_id)
    parent = f"projects/{project}/locations/global"

    # Tell the API where to send a notification when the job is complete.
    actions = [{"pub_sub": {"topic": topic}}]

    # Construct the inspect_job, which defines the entire inspect content task.
    inspect_job = {
        "inspect_config": inspect_config,
        "storage_config": storage_config,
        "actions": actions,
    }

    operation = dlp.create_dlp_job(
        request={"parent": parent, "inspect_job": inspect_job}
    )
    print(f"Inspection operation started: {operation.name}")

    # Create a Pub/Sub client and find the subscription. The subscription is
    # expected to already be listening to the topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_id)

    # Set up a callback to acknowledge a message. This closes around an event
    # so that it can signal that it is done and the main thread can continue.
    job_done = threading.Event()

    def callback(message: google.cloud.pubsub_v1.subscriber.message.Message) -> None:
        try:
            if message.attributes["DlpJobName"] == operation.name:
                # This is the message we're looking for, so acknowledge it.
                message.ack()

                # Now that the job is done, fetch the results and print them.
                job = dlp.get_dlp_job(request={"name": operation.name})
                print(f"Job name: {job.name}")
                if job.inspect_details.result.info_type_stats:
                    for finding in job.inspect_details.result.info_type_stats:
                        print(
                            "Info type: {}; Count: {}".format(
                                finding.info_type.name, finding.count
                            )
                        )
                else:
                    print("No findings.")

                # Signal to the main thread that we can exit.
                job_done.set()
            else:
                # This is not the message we're looking for.
                message.drop()
        except Exception as e:
            # Because this is executing in a thread, an exception won't be
            # noted unless we print it manually.
            print(e)
            raise

    # Register the callback and wait on the event.
    subscriber.subscribe(subscription_path, callback=callback)
    finished = job_done.wait(timeout=timeout)
    if not finished:
        print(
            "No event received before the timeout. Please verify that the "
            "subscription provided is subscribed to the topic provided."
        )


# [END dlp_inspect_bigquery]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "bigquery_project",
        help="The Google Cloud project id of the target table.",
    )
    parser.add_argument("dataset_id", help="The ID of the target BigQuery dataset.")
    parser.add_argument("table_id", help="The ID of the target BigQuery table.")
    parser.add_argument(
        "topic_id",
        help="The id of the Cloud Pub/Sub topic to use to report that the job "
        'is complete, e.g. "dlp-sample-topic".',
    )
    parser.add_argument(
        "subscription_id",
        help="The id of the Cloud Pub/Sub subscription to monitor for job "
        'completion, e.g. "dlp-sample-subscription". The subscription must '
        "already be subscribed to the topic. See the test files or the Cloud "
        "Pub/Sub sample files for examples on how to create the subscription.",
    )
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser.add_argument(
        "--min_likelihood",
        choices=[
            "LIKELIHOOD_UNSPECIFIED",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ],
        help="A string representing the minimum likelihood threshold that "
        "constitutes a match.",
    )
    parser.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="The maximum number of seconds to wait for a response from the "
        "API. The default is 300 seconds.",
        default=300,
    )

    args = parser.parse_args()

    inspect_bigquery(
        args.project,
        args.bigquery_project,
        args.dataset_id,
        args.table_id,
        args.topic_id,
        args.subscription_id,
        args.info_types,
        custom_dictionaries=args.custom_dictionaries,
        custom_regexes=args.custom_regexes,
        min_likelihood=args.min_likelihood,
        max_findings=args.max_findings,
        timeout=args.timeout,
    )

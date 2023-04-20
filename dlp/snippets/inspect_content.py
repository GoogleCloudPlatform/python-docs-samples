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

from __future__ import print_function
from typing import List

import argparse
import json
import os


# [START dlp_inspect_string_basic]
def inspect_string_basic(
    project,
    content_string,
    info_types=["PHONE_NUMBER"],
):
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration dictionary.
    inspect_config = {
        "info_types": info_types,
        "include_quote": True,
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            print("Quote: {}".format(finding.quote))
            print("Info type: {}".format(finding.info_type.name))
            print("Likelihood: {}".format(finding.likelihood))
    else:
        print("No findings.")


# [END dlp_inspect_string_basic]


# [START dlp_inspect_string]
def inspect_string(
    project,
    content_string,
    info_types,
    custom_dictionaries=None,
    custom_regexes=None,
    min_likelihood=None,
    max_findings=None,
    include_quote=True,
):
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare custom_info_types by parsing the dictionary word lists and
    # regex patterns.
    if custom_dictionaries is None:
        custom_dictionaries = []
    dictionaries = [
        {
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
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
        "include_quote": include_quote,
        "limits": {"max_findings_per_request": max_findings},
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            try:
                if finding.quote:
                    print("Quote: {}".format(finding.quote))
            except AttributeError:
                pass
            print("Info type: {}".format(finding.info_type.name))
            print("Likelihood: {}".format(finding.likelihood))
    else:
        print("No findings.")


# [END dlp_inspect_string]

# [START dlp_inspect_table]


def inspect_table(
    project,
    data,
    info_types,
    custom_dictionaries=None,
    custom_regexes=None,
    min_likelihood=None,
    max_findings=None,
    include_quote=True,
):
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        data: Json string representing table data.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    Returns:
        None; the response from the API is printed to the terminal.
    Example:
        data = {
            "header":[
                "email",
                "phone number"
            ],
            "rows":[
                [
                    "robertfrost@xyz.com",
                    "4232342345"
                ],
                [
                    "johndoe@pqr.com",
                    "4253458383"
                ]
            ]
        }

        >> $ python inspect_content.py table \
        '{"header": ["email", "phone number"],
        "rows": [["robertfrost@xyz.com", "4232342345"],
        ["johndoe@pqr.com", "4253458383"]]}'
        >>  Quote: robertfrost@xyz.com
            Info type: EMAIL_ADDRESS
            Likelihood: 4
            Quote: johndoe@pqr.com
            Info type: EMAIL_ADDRESS
            Likelihood: 4
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare custom_info_types by parsing the dictionary word lists and
    # regex patterns.
    if custom_dictionaries is None:
        custom_dictionaries = []
    dictionaries = [
        {
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
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
        "include_quote": include_quote,
        "limits": {"max_findings_per_request": max_findings},
    }

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in data["header"]]
    rows = []
    for row in data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {}
    table["headers"] = headers
    table["rows"] = rows
    item = {"table": table}
    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            try:
                if finding.quote:
                    print("Quote: {}".format(finding.quote))
            except AttributeError:
                pass
            print("Info type: {}".format(finding.info_type.name))
            print("Likelihood: {}".format(finding.likelihood))
    else:
        print("No findings.")


# [END dlp_inspect_table]

# [START dlp_inspect_file]


def inspect_file(
    project,
    filename,
    info_types,
    min_likelihood=None,
    custom_dictionaries=None,
    custom_regexes=None,
    max_findings=None,
    include_quote=True,
    mime_type=None,
):
    """Uses the Data Loss Prevention API to analyze a file for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
        mime_type: The MIME type of the file. If not specified, the type is
            inferred via the Python standard library's mimetypes module.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    import mimetypes

    # Import the client library.
    import google.cloud.dlp

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
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
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
        "include_quote": include_quote,
        "limits": {"max_findings_per_request": max_findings},
    }

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0]

    # Select the content type index from the list of supported types.
    supported_content_types = {
        None: 0,  # "Unspecified"
        "image/jpeg": 1,
        "image/bmp": 2,
        "image/png": 3,
        "image/svg": 4,
        "text/plain": 5,
    }
    content_type_index = supported_content_types.get(mime_type, 0)

    # Construct the item, containing the file's byte data.
    with open(filename, mode="rb") as f:
        item = {"byte_item": {"type_": content_type_index, "data": f.read()}}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            try:
                print("Quote: {}".format(finding.quote))
            except AttributeError:
                pass
            print("Info type: {}".format(finding.info_type.name))
            print("Likelihood: {}".format(finding.likelihood))
    else:
        print("No findings.")


# [END dlp_inspect_file]


# [START dlp_inspect_gcs]
def inspect_gcs_file(
    project,
    bucket,
    filename,
    topic_id,
    subscription_id,
    info_types,
    custom_dictionaries=None,
    custom_regexes=None,
    min_likelihood=None,
    max_findings=None,
    timeout=300,
):
    """Uses the Data Loss Prevention API to analyze a file on GCS.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        bucket: The name of the GCS bucket containing the file, as a string.
        filename: The name of the file in the bucket, including the path, as a
            string; e.g. 'images/myfile.png'.
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

    # Import the client library.
    # This sample also uses threading.Event() to wait for the job to finish.
    import threading

    import google.cloud.dlp

    # This sample additionally uses Cloud Pub/Sub to receive results from
    # potentially long-running operations.
    import google.cloud.pubsub

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
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
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

    # Construct a storage_config containing the file's URL.
    url = "gs://{}/{}".format(bucket, filename)
    storage_config = {"cloud_storage_options": {"file_set": {"url": url}}}

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
    print("Inspection operation started: {}".format(operation.name))

    # Create a Pub/Sub client and find the subscription. The subscription is
    # expected to already be listening to the topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_id)

    # Set up a callback to acknowledge a message. This closes around an event
    # so that it can signal that it is done and the main thread can continue.
    job_done = threading.Event()

    def callback(message):
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

    subscriber.subscribe(subscription_path, callback=callback)
    finished = job_done.wait(timeout=timeout)
    if not finished:
        print(
            "No event received before the timeout. Please verify that the "
            "subscription provided is subscribed to the topic provided."
        )


# [END dlp_inspect_gcs]


# [START dlp_inspect_datastore]
def inspect_datastore(
    project,
    datastore_project,
    kind,
    topic_id,
    subscription_id,
    info_types,
    custom_dictionaries=None,
    custom_regexes=None,
    namespace_id=None,
    min_likelihood=None,
    max_findings=None,
    timeout=300,
):
    """Uses the Data Loss Prevention API to analyze Datastore data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        datastore_project: The Google Cloud project id of the target Datastore.
        kind: The kind of the Datastore entity to inspect, e.g. 'Person'.
        topic_id: The id of the Cloud Pub/Sub topic to which the API will
            broadcast job completion. The topic must already exist.
        subscription_id: The id of the Cloud Pub/Sub subscription to listen on
            while waiting for job completion. The subscription must already
            exist and be subscribed to the topic.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        namespace_id: The namespace of the Datastore document, if applicable.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        timeout: The number of seconds to wait for a response from the API.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    # This sample also uses threading.Event() to wait for the job to finish.
    import threading

    import google.cloud.dlp

    # This sample additionally uses Cloud Pub/Sub to receive results from
    # potentially long-running operations.
    import google.cloud.pubsub

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
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
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

    # Construct a storage_config containing the target Datastore info.
    storage_config = {
        "datastore_options": {
            "partition_id": {
                "project_id": datastore_project,
                "namespace_id": namespace_id,
            },
            "kind": {"name": kind},
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
    print("Inspection operation started: {}".format(operation.name))

    # Create a Pub/Sub client and find the subscription. The subscription is
    # expected to already be listening to the topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_id)

    # Set up a callback to acknowledge a message. This closes around an event
    # so that it can signal that it is done and the main thread can continue.
    job_done = threading.Event()

    def callback(message):
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


# [END dlp_inspect_datastore]


# [START dlp_inspect_bigquery]
def inspect_bigquery(
    project,
    bigquery_project,
    dataset_id,
    table_id,
    topic_id,
    subscription_id,
    info_types,
    custom_dictionaries=None,
    custom_regexes=None,
    min_likelihood=None,
    max_findings=None,
    timeout=500,
):
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
        namespace_id: The namespace of the Datastore document, if applicable.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        timeout: The number of seconds to wait for a response from the API.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    # This sample also uses threading.Event() to wait for the job to finish.
    import threading

    import google.cloud.dlp

    # This sample additionally uses Cloud Pub/Sub to receive results from
    # potentially long-running operations.
    import google.cloud.pubsub

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
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
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
    print("Inspection operation started: {}".format(operation.name))

    # Create a Pub/Sub client and find the subscription. The subscription is
    # expected to already be listening to the topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_id)

    # Set up a callback to acknowledge a message. This closes around an event
    # so that it can signal that it is done and the main thread can continue.
    job_done = threading.Event()

    def callback(message):
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


# [START dlp_inspect_bigquery_with_sampling]
def inspect_bigquery_table_with_sampling(
    project: str,
    bigquery_project: str,
    dataset_id: str,
    table_id: str,
    topic_id: str,
    subscription_id: str,
    info_types: List[str] = None,
    min_likelihood: str = None,
    max_findings: str = None,
    timeout: int =300,
) -> None:
    """Uses the Data Loss Prevention API to analyze BigQuery data by limiting
    the amount of data to be scanned.
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
    """

    # This sample also uses threading.Event() to wait for the job to finish.
    import threading

    # Import the client library.
    import google.cloud.dlp

    # This sample additionally uses Cloud Pub/Sub to receive results from
    # potentially long-running operations.
    import google.cloud.pubsub

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    if not info_types:
        info_types = ["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"]
    info_types = [{"name": info_type} for info_type in info_types]

    # Specify how the content should be inspected. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": min_likelihood,
        "limits": {"max_findings_per_request": max_findings},
        "include_quote": True
    }

    # Specify the BigQuery table to be inspected.
    table_reference = {
        "project_id": bigquery_project,
        "dataset_id": dataset_id,
        "table_id": table_id,
    }

    # Construct a storage_config containing the target BigQuery info.
    storage_config = {
        "big_query_options": {
            "table_reference": table_reference,
            "rows_limit": 1000,
            "sample_method": 'RANDOM_START',
            "identifying_fields": [{"name": "name"}]
        }
    }

    # Tell the API where to send a notification when the job is complete.
    topic = google.cloud.pubsub.PublisherClient.topic_path(project, topic_id)
    actions = [{"pub_sub": {"topic": topic}}]

    # Construct the inspect_job, which defines the entire inspect content task.
    inspect_job = {
        "inspect_config": inspect_config,
        "storage_config": storage_config,
        "actions": actions,
    }

    # Convert the project id into full resource ids.
    parent = f"projects/{project}/locations/global"

    # Call the API
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

    def callback(message):
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

# [END dlp_inspect_bigquery_with_sampling]


if __name__ == "__main__":
    default_project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="content", help="Select how to submit content to the API."
    )
    subparsers.required = True

    parser_string = subparsers.add_parser("string", help="Inspect a string.")
    parser_string.add_argument("item", help="The string to inspect.")
    parser_string.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_string.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_string.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser_string.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser_string.add_argument(
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
    parser_string.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_string.add_argument(
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )

    parser_table = subparsers.add_parser("table", help="Inspect a table.")
    parser_table.add_argument(
        "data", help="Json string representing a table.", type=json.loads
    )
    parser_table.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_table.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_table.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser_table.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser_table.add_argument(
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
    parser_table.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_table.add_argument(
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )

    parser_file = subparsers.add_parser("file", help="Inspect a local file.")
    parser_file.add_argument("filename", help="The path to the file to inspect.")
    parser_file.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_file.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_file.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser_file.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser_file.add_argument(
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
    parser_file.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_file.add_argument(
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )
    parser_file.add_argument(
        "--mime_type",
        help="The MIME type of the file. If not specified, the type is "
        "inferred via the Python standard library's mimetypes module.",
    )

    parser_gcs = subparsers.add_parser(
        "gcs", help="Inspect files on Google Cloud Storage."
    )
    parser_gcs.add_argument(
        "bucket", help="The name of the GCS bucket containing the file."
    )
    parser_gcs.add_argument(
        "filename",
        help="The name of the file in the bucket, including the path, e.g. "
        '"images/myfile.png". Wildcards are permitted.',
    )
    parser_gcs.add_argument(
        "topic_id",
        help="The id of the Cloud Pub/Sub topic to use to report that the job "
        'is complete, e.g. "dlp-sample-topic".',
    )
    parser_gcs.add_argument(
        "subscription_id",
        help="The id of the Cloud Pub/Sub subscription to monitor for job "
        'completion, e.g. "dlp-sample-subscription". The subscription must '
        "already be subscribed to the topic. See the test files or the Cloud "
        "Pub/Sub sample files for examples on how to create the subscription.",
    )
    parser_gcs.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_gcs.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_gcs.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser_gcs.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser_gcs.add_argument(
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
    parser_gcs.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_gcs.add_argument(
        "--timeout",
        type=int,
        help="The maximum number of seconds to wait for a response from the "
        "API. The default is 300 seconds.",
        default=300,
    )

    parser_datastore = subparsers.add_parser(
        "datastore", help="Inspect files on Google Datastore."
    )
    parser_datastore.add_argument(
        "datastore_project",
        help="The Google Cloud project id of the target Datastore.",
    )
    parser_datastore.add_argument(
        "kind",
        help='The kind of the Datastore entity to inspect, e.g. "Person".',
    )
    parser_datastore.add_argument(
        "topic_id",
        help="The id of the Cloud Pub/Sub topic to use to report that the job "
        'is complete, e.g. "dlp-sample-topic".',
    )
    parser_datastore.add_argument(
        "subscription_id",
        help="The id of the Cloud Pub/Sub subscription to monitor for job "
        'completion, e.g. "dlp-sample-subscription". The subscription must '
        "already be subscribed to the topic. See the test files or the Cloud "
        "Pub/Sub sample files for examples on how to create the subscription.",
    )
    parser_datastore.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_datastore.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_datastore.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser_datastore.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser_datastore.add_argument(
        "--namespace_id", help="The Datastore namespace to use, if applicable."
    )
    parser_datastore.add_argument(
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
    parser_datastore.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_datastore.add_argument(
        "--timeout",
        type=int,
        help="The maximum number of seconds to wait for a response from the "
        "API. The default is 300 seconds.",
        default=300,
    )

    parser_bigquery = subparsers.add_parser(
        "bigquery", help="Inspect files on Google BigQuery."
    )
    parser_bigquery.add_argument(
        "bigquery_project",
        help="The Google Cloud project id of the target table.",
    )
    parser_bigquery.add_argument(
        "dataset_id", help="The ID of the target BigQuery dataset."
    )
    parser_bigquery.add_argument(
        "table_id", help="The ID of the target BigQuery table."
    )
    parser_bigquery.add_argument(
        "topic_id",
        help="The id of the Cloud Pub/Sub topic to use to report that the job "
        'is complete, e.g. "dlp-sample-topic".',
    )
    parser_bigquery.add_argument(
        "subscription_id",
        help="The id of the Cloud Pub/Sub subscription to monitor for job "
        'completion, e.g. "dlp-sample-subscription". The subscription must '
        "already be subscribed to the topic. See the test files or the Cloud "
        "Pub/Sub sample files for examples on how to create the subscription.",
    )
    parser_bigquery.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_bigquery.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_bigquery.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser_bigquery.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser_bigquery.add_argument(
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
    parser_bigquery.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_bigquery.add_argument(
        "--timeout",
        type=int,
        help="The maximum number of seconds to wait for a response from the "
        "API. The default is 300 seconds.",
        default=300,
    )

    parser_bigquery_with_sampling = subparsers.add_parser(
        "bigquery_with_sampling",
        help="Inspect files on Google BigQuery by limiting the amount of "
        "data to be scanned."
    )
    parser_bigquery_with_sampling.add_argument(
        "bigquery_project",
        help="The Google Cloud project id of the target table.",
    )
    parser_bigquery_with_sampling.add_argument(
        "dataset_id", help="The ID of the target BigQuery dataset."
    )
    parser_bigquery_with_sampling.add_argument(
        "table_id", help="The ID of the target BigQuery table."
    )
    parser_bigquery_with_sampling.add_argument(
        "topic_id",
        help="The id of the Cloud Pub/Sub topic to use to report that the job "
        'is complete, e.g. "dlp-sample-topic".',
    )
    parser_bigquery_with_sampling.add_argument(
        "subscription_id",
        help="The id of the Cloud Pub/Sub subscription to monitor for job "
        'completion, e.g. "dlp-sample-subscription". The subscription must '
        "already be subscribed to the topic. See the test files or the Cloud "
        "Pub/Sub sample files for examples on how to create the subscription.",
    )
    parser_bigquery_with_sampling.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_bigquery_with_sampling.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_bigquery_with_sampling.add_argument(
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
    parser_bigquery_with_sampling.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_bigquery_with_sampling.add_argument(
        "--timeout",
        type=int,
        help="The maximum number of seconds to wait for a response from the "
        "API. The default is 300 seconds.",
        default=300,
    )

    args = parser.parse_args()

    if args.content == "string":
        inspect_string(
            args.project,
            args.item,
            args.info_types,
            custom_dictionaries=args.custom_dictionaries,
            custom_regexes=args.custom_regexes,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            include_quote=args.include_quote,
        )
    elif args.content == "table":
        inspect_table(
            args.project,
            args.data,
            args.info_types,
            custom_dictionaries=args.custom_dictionaries,
            custom_regexes=args.custom_regexes,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            include_quote=args.include_quote,
        )
    elif args.content == "file":
        inspect_file(
            args.project,
            args.filename,
            args.info_types,
            custom_dictionaries=args.custom_dictionaries,
            custom_regexes=args.custom_regexes,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            include_quote=args.include_quote,
            mime_type=args.mime_type,
        )
    elif args.content == "gcs":
        inspect_gcs_file(
            args.project,
            args.bucket,
            args.filename,
            args.topic_id,
            args.subscription_id,
            args.info_types,
            custom_dictionaries=args.custom_dictionaries,
            custom_regexes=args.custom_regexes,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            timeout=args.timeout,
        )
    elif args.content == "datastore":
        inspect_datastore(
            args.project,
            args.datastore_project,
            args.kind,
            args.topic_id,
            args.subscription_id,
            args.info_types,
            custom_dictionaries=args.custom_dictionaries,
            custom_regexes=args.custom_regexes,
            namespace_id=args.namespace_id,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            timeout=args.timeout,
        )
    elif args.content == "bigquery":
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
    elif args.content == "bigquery_with_sampling":
        inspect_bigquery_table_with_sampling(
            args.project,
            args.bigquery_project,
            args.dataset_id,
            args.table_id,
            args.topic_id,
            args.subscription_id,
            info_types=args.info_types,
            min_likelihood=args.min_likelihood,
            max_findings=args.max_findings,
            timeout=args.timeout,
        )

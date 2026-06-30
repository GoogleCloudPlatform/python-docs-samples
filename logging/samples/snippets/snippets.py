#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""This application demonstrates how to perform basic operations on logs and
log entries with Cloud Logging.

For more information, see the README.md under /logging and the
documentation at https://cloud.google.com/logging/docs.
"""

import argparse
import time

import google.cloud.logging

import logging


# [START logging_write_log_entry]
def write_entry():
    """Demonstrates how to write log entries to Google Cloud using Python's standard logging library."""
    logging_client = google.cloud.logging.Client()

    # Logs default to projects/[PROJECT_ID]/logs/python unless routed
    # differently by a custom handler or managed GCP infrastructure.
    logging_client.setup_logging(log_level=logging.INFO)

    # Make a simple text log
    logging.info("Hello, world!")

    # Simple text log with severity.
    logging.warning("Goodbye, world!")

    # Prepare your structured data as a dictionary.
    json_log = {
        "name": "King Arthur",
        "quest": "Find the Holy Grail",
        "favorite_color": "Blue",
    }

    logging.info("This is a JSON log.", extra={"json_fields": json_log})

    # wait for threads to finish working on the background.
    time.sleep(5)


# [END logging_write_log_entry]


# [START logging_list_log_entries]
def list_entries(logger_name):
    """Lists the most recent entries for a given logger."""
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    print("Listing entries for logger {}:".format(logger.name))

    for entry in logger.list_entries():
        timestamp = entry.timestamp.isoformat()
        print("* {}: {}".format(timestamp, entry.payload))


# [END logging_list_log_entries]


# [START logging_delete_log]
def delete_logger(logger_name):
    """Deletes a logger and all its entries.

    Note that a deletion can take several minutes to take effect.
    """
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    logger.delete()

    print("Deleted all logging entries for {}".format(logger.name))


# [END logging_delete_log]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("logger_name", help="Logger name", default="example_log")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help=list_entries.__doc__)
    subparsers.add_parser("write", help=write_entry.__doc__)
    subparsers.add_parser("delete", help=delete_logger.__doc__)

    args = parser.parse_args()

    if args.command == "list":
        list_entries(args.logger_name)
    elif args.command == "write":
        write_entry()
    elif args.command == "delete":
        delete_logger(args.logger_name)

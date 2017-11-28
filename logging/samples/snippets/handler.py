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


def use_logging_handler():
    # [START logging_handler_setup]
    # Imports the Google Cloud client library
    import google.cloud.logging

    # Instantiates a client
    client = google.cloud.logging.Client()

    # Connects the logger to the root logging handler; by default this captures
    # all logs at INFO level and higher
    client.setup_logging()
    # [END logging_handler_setup]

    # [START logging_handler_usage]
    # Imports Python standard library logging
    import logging

    # The data to log
    text = 'Hello, world!'

    # Emits the data using the standard logging module
    logging.warn(text)
    # [END logging_handler_usage]

    print('Logged: {}'.format(text))


if __name__ == '__main__':
    use_logging_handler()

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START logging_get_sink]
from typing import List
from google.cloud import logging


def get_sink(project_id: str, sink_name: str) -> logging.Sink:
    """Retrieves the metadata for a Cloud Logging Sink.

    Args:
        project_id: the ID of the project
        sink_name: the name of the sink

    Returns:
        A Cloud Logging Sink.
    """
    client = logging.Client(project=project_id)
    sink = client.sink(sink_name)
    sink.reload()
    print(f"Name: {sink.name}")
    print(f"Destination: {sink.destination}")
    print(f"Filter: {sink.filter_}")
    return sink


# [END logging_get_sink]

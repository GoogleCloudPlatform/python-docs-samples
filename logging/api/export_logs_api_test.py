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

from collections import namedtuple

import export_logs_api

SINK_NAME = 'test_sink'


def test_sinks(cloud_config):
    client = export_logs_api.get_client(cloud_config.project)

    Args = namedtuple('Args', 'project_id destination_bucket sink_name')
    args = Args(
        destination_bucket=cloud_config.storage_bucket,
        project_id=cloud_config.project,
        sink_name=SINK_NAME)

    export_logs_api.create_sink_if_not_exists(client, args)
    sinks = export_logs_api.list_sinks(client, args)
    matched_sinks = [s for s in sinks if s.name == SINK_NAME]
    assert len(matched_sinks) == 1
    export_logs_api.update_sink(client, args)
    export_logs_api.delete_sink(client, args)

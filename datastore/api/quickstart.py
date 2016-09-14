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

# [START datastore_quickstart]
# Imports the Google Cloud client library
from google.cloud import datastore

# Instantiates a client
datastore_client = datastore.Client()

# The kind of the entity to retrieve
kind = 'Task'
# The id of the entity to retrieve
id = 1234567890
# The Datastore key for the entity
task_key = datastore_client.key(kind, id)

# Retrieves the entity
entity = datastore_client.get(task_key)

print('Got entity: {}'.format(entity.key.id))
# [END datastore_quickstart]

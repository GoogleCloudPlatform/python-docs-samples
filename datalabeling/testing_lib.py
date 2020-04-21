# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import datalabeling_v1beta1 as datalabeling


def create_client():
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if 'DATALABELING_ENDPOINT' in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv('DATALABELING_ENDPOINT'))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    else:
        client = datalabeling.DataLabelingServiceClient()
    return client


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=60)
def delete_annotation_spec_set(name):
    client = create_client()
    client.delete_annotation_spec_set(name)

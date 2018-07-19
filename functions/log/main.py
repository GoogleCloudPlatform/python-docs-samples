# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_log_helloworld]
import logging


def hello_world(event, context):
    """Background Cloud Function.
    Args:
         event (dict): The dictionary with data specific to the given event.
         context (google.cloud.functions.Context): The Cloud Functions event
         context.
    """
    print('Hello, stdout!')
    logging.warn('Hello, logging handler!')
# [END functions_log_helloworld]

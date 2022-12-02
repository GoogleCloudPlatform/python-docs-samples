# Copyright 2022 Google LLC
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

from setup_cleanup import delete_bucket


def delete_bucket_by_name(name: str):
    if name is None:
        bucket_name = os.getenv("EVENTS_BUCKET_NAME")
        delete_bucket(bucket_name)
    else:
        delete_bucket(name)

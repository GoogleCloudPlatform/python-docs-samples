# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff

from google.api_core.exceptions import ResourceExhausted

import get_short_form_image_captions


_RESOURCES = os.path.join(os.path.dirname(__file__), "test_resources")
_INPUT_FILE = os.path.join(_RESOURCES, "cat.png")


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=60)
def test_get_short_form_image_captions() -> None:
    response = get_short_form_image_captions.get_short_form_image_captions(
        _INPUT_FILE,
    )

    assert len(response) > 0 and "cat" in response[0]

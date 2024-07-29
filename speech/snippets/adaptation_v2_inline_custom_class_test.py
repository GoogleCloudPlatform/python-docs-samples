# Copyright 2022 Google LLC
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
import re

from google.api_core.retry import Retry

import adaptation_v2_inline_custom_class

_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_adaptation_v2_inline_custom_class() -> None:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    response = adaptation_v2_inline_custom_class.adaptation_v2_inline_custom_class(
        project_id, os.path.join(_RESOURCES, "fair.wav")
    )

    assert re.search(
        r"the word",
        response.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )

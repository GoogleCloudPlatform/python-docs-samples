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

import verify_image_watermark


_RESOURCES = os.path.join(os.path.dirname(__file__), "test_resources")
_INPUT_FILE_WATERMARK = os.path.join(_RESOURCES, "dog_newspaper.png")
_INPUT_FILE_NO_WATERMARK = os.path.join(_RESOURCES, "dog_book.png")


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=60)
def test_verify_image_watermark() -> None:
    response = verify_image_watermark.verify_image_watermark(
        _INPUT_FILE_WATERMARK,
    )

    assert (
        len(response.watermark_verification_result) > 0
        and "ACCEPT" in response.watermark_verification_result
    )

    response = verify_image_watermark.verify_image_watermark(
        _INPUT_FILE_NO_WATERMARK,
    )

    assert (
        len(response.watermark_verification_result) > 0
        and "REJECT" in response.watermark_verification_result
    )

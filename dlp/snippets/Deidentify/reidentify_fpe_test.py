# Copyright 2023 Google LLC
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
import os

import pytest

import reidentify_fpe as reid

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
WRAPPED_KEY = (
    "CiQAz0hX4+go8fJwn80Fr8pVImwx+tmZdqU7JL+7TN/S5JxBU9gSSQDhFHpFVy"
    "uzJps0YH9ls480mU+JLG7jI/0lL04i6XJRWqmI6gUSZRUtECYcLH5gXK4SXHlL"
    "rotx7Chxz/4z7SIpXFOBY61z0/U="
)
KEY_NAME = (
    f"projects/{GCLOUD_PROJECT}/locations/global/keyRings/"
    "dlp-test/cryptoKeys/dlp-test"
)
SURROGATE_TYPE = "SSN_TOKEN"


def test_reidentify_with_fpe(capsys: pytest.CaptureFixture) -> None:
    labeled_fpe_string = "My SSN is SSN_TOKEN(9):731997681"

    reid.reidentify_with_fpe(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        surrogate_type=SURROGATE_TYPE,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
        alphabet="NUMERIC",
    )

    out, _ = capsys.readouterr()

    assert "731997681" not in out

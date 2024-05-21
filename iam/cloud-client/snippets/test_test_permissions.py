# Copyright 2024 Google LLC
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
import google.auth

from .iam_check_permissions import test_permissions as sample_test_permissions

PROJECT = google.auth.default()[1]


def test_test_permissions() -> None:
    perms = sample_test_permissions(PROJECT)
    assert "resourcemanager.projects.get" in perms

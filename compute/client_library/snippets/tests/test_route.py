#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import uuid

import google.auth
import pytest

from ..routes.create_kms_route import create_route_to_windows_activation_host
from ..routes.delete import delete_route
from ..routes.list import list_routes

PROJECT = google.auth.default()[1]


def test_route_create_delete():
    route_name = "test-route" + uuid.uuid4().hex[:10]
    route = create_route_to_windows_activation_host(PROJECT, "global/networks/default", route_name)
    try:
        assert route.name == route_name
        assert route.dest_range == "35.190.247.13/32"
    finally:

        delete_route(PROJECT, route_name)

        for route in list_routes(PROJECT):
            if route.name == route_name:
                pytest.fail(f"Failed to delete test route {route_name}.")

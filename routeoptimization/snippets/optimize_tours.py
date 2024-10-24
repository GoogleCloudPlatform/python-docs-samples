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

# [START routeoptimization_optimize_tours_basic]

from google.maps import routeoptimization_v1


def call_optimize_tours(project_id: str) -> None:
    # Use Default Application Credentials for the environment.
    client = routeoptimization_v1.RouteOptimizationClient()

    response = client.optimize_tours(
        request=routeoptimization_v1.OptimizeToursRequest(
            parent="projects/" + project_id,
            model={
                "shipments": [
                    {
                        "deliveries": [
                            {
                                "arrival_location": {
                                    "latitude": 48.880942,
                                    "longitude": 2.323866,
                                }
                            }
                        ]
                    }
                ],
                "vehicles": [
                    {
                        "end_location": {"latitude": 48.86311, "longitude": 2.341205},
                        "start_location": {
                            "latitude": 48.863102,
                            "longitude": 2.341204,
                        },
                    }
                ],
            },
        )
    )

    return response


# [END routeoptimization_optimize_tours_basic]

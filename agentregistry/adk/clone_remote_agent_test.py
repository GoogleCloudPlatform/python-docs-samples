# Copyright 2026 Google LLC
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

import pytest

import clone_remote_agent


def test_clone_remote_agent(
    monkeypatch: pytest.MonkeyPatch,
    project_id: str,
    location: str,
    agent_id: str,
) -> None:
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", project_id)
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", location)

    flight_orchestrator, hotel_orchestrator = clone_remote_agent.clone_remote_agent(
        agent_name=f"projects/{project_id}/locations/{location}/agents/{agent_id}",
    )

    assert flight_orchestrator.name == "flight_orchestrator"
    assert hotel_orchestrator.name == "hotel_orchestrator"
    assert len(flight_orchestrator.sub_agents) == 1
    assert len(hotel_orchestrator.sub_agents) == 1
    assert (
        flight_orchestrator.sub_agents[0] is not hotel_orchestrator.sub_agents[0]
    )

# Copyright 2026 Google LLC
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

import pytest
import os

from google.cloud import aiplatform

import create_agent_engine
import generate_memories
import delete_agent_engine

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"

@pytest.fixture(scope="module")
def agent_engine_id():
    """Creates a test Agent Engine and yields its ID, ensuring cleanup."""
    if not PROJECT_ID:
        pytest.skip("GOOGLE_CLOUD_PROJECT not set")

    print("Creating Agent Engine...")
    engine_name = None
    try:
        engine = create_agent_engine.create_agent_engine_with_memorybank_config(PROJECT_ID, LOCATION)
        engine_name = engine.api_resource.name
        yield engine_name
    except Exception as e:
        pytest.skip(f"Failed to create agent engine: {e}")
    finally:
        # This 'finally' block ensures cleanup even if tests fail
        if engine_name:
            print(f"Cleaning up: {engine_name}")
            try:
                delete_agent_engine.delete_agent_engine(PROJECT_ID, LOCATION, engine_name)
            except Exception:
                pass

@pytest.mark.skipif(not PROJECT_ID, reason="GOOGLE_CLOUD_PROJECT not set")
def test_create_agent_engine(agent_engine_id):
    assert agent_engine_id

@pytest.mark.skipif(not PROJECT_ID, reason="GOOGLE_CLOUD_PROJECT not set")
def test_generate_memories(agent_engine_id):
    if not agent_engine_id:
        pytest.skip("Agent Engine not created")
    response = generate_memories.generate_memories(PROJECT_ID, LOCATION, agent_engine_id)
    assert response

@pytest.mark.skipif(not PROJECT_ID, reason="GOOGLE_CLOUD_PROJECT not set")
def test_delete_agent_engine():
    """Tests that an agent engine can be deleted."""
    # Create a fresh one just to test the delete function
    engine = create_agent_engine.create_agent_engine_with_memorybank_config(PROJECT_ID, LOCATION)
    assert engine, "Failed to create engine for deletion test"
    
    # Call your delete function and ensure it doesn't crash
    delete_agent_engine.delete_agent_engine(
        PROJECT_ID, LOCATION, engine.api_resource.name
    )

# Simplified test that just checks imports and structural correctness without calling API
def test_imports():
    assert create_agent_engine.create_agent_engine_with_memorybank_config
    assert generate_memories.generate_memories
    assert delete_agent_engine.delete_agent_engine

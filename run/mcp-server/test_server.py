# Copyright 2025 Google LLC
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

# [START cloudrun_mcpserver_test_otel]
from otel_setup import setup_opentelemetry
setup_opentelemetry("test-server")

# [START cloudrun_mcpserver_test]
import asyncio

from fastmcp import Client


async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.
    async with Client("http://localhost:8080/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f">>> 🛠️  Tool found: {tool.name}")
        # Call add tool
        print(">>> 🪛  Calling add tool for 1 + 2")
        result = await client.call_tool("add", {"a": 1, "b": 2})
        print(f"<<< ✅ Result: {result.content[0].text}")
        # Call subtract tool
        print(">>> 🪛  Calling subtract tool for 10 - 3")
        result = await client.call_tool("subtract", {"a": 10, "b": 3})
        print(f"<<< ✅ Result: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(test_server())
# [END cloudrun_mcpserver_test]
# [END cloudrun_mcpserver_test_otel]
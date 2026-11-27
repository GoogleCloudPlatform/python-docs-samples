Agent Registry Python Samples
=============================

Code samples for `Google Cloud Agent Registry`_, using the Agent Development Kit (ADK) and Vertex AI Agent Engine.

.. _Google Cloud Agent Registry: https://cloud.google.com/agent-registry

Quick Start
-----------

1. Select or create a Google Cloud project.
2. Enable billing for your project.
3. Enable the Agent Registry API (`agentregistry.googleapis.com`) and Vertex AI API (`aiplatform.googleapis.com`).
4. Set up `Application Default Credentials`_.
5. Set the required environment variables and install dependencies:

   .. code-block:: bash

      export GOOGLE_CLOUD_PROJECT="your-project-id"
      export GOOGLE_CLOUD_LOCATION="global"
      cd adk
      pip install -r requirements.txt

.. _Application Default Credentials: https://googleapis.dev/python/google-api-core/latest/auth.html

Samples
-------

* `adk/compose_multi_agent.py`: Initialize the ``AgentRegistry`` client and compose an ``LlmAgent`` orchestrator with a remote A2A agent and an MCP toolset.
* `adk/clone_remote_agent.py`: Fetch a remote A2A agent once and clone it across multiple orchestrator agents.
* `adk/discover_agents_and_toolsets.py`: Discover agents by skill tag and retrieve remote agents and MCP toolsets.
* `adk/deploy_agent_runtime.py`: Deploy an A2A agent to Vertex AI Agent Engine so it is automatically registered in Agent Registry.

Testing
-------

Tests require a Google Cloud project with ``agentregistry.googleapis.com`` enabled and the following environment variables set:

* ``GOOGLE_CLOUD_PROJECT``: Google Cloud project ID.
* ``GOOGLE_CLOUD_LOCATION``: Agent Registry location (defaults to ``global``).
* ``AGENTREGISTRY_TEST_AGENT_ID``: ID of a pre-registered A2A agent fixture.
* ``AGENTREGISTRY_TEST_MCP_SERVER_ID``: ID of a pre-registered MCP server fixture.
* ``AGENTREGISTRY_TEST_STAGING_BUCKET``: Cloud Storage bucket URI (``gs://...``) for the Agent Engine deployment test.

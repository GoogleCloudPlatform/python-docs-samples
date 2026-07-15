# Data Engineering Agent A2A Client Example

This directory contains a sample Python implementation of an
[Agent-to-Agent (A2A)](https://a2a-protocol.org/) client designed to interact
with the **Google Cloud Data Engineering Agent (DEA)**.

## Background

The Data Engineering Agent is a BigQuery and Dataform ELT expert capable of
building, managing, and troubleshooting data pipelines. To enable
interoperability across different platforms and agents, it exposes an interface
following the A2A protocol.

Official Documentation:
[Data Engineering Agent API Overview](https://docs.cloud.google.com/gemini/data-agents/data-engineering-agent/api-overview)

This example demonstrates how to use the open-source
[A2A Python SDK](https://github.com/a2aproject/a2a-python) to:

1. **Discover** the agent's capabilities via its Agent Card.
2. **Authenticate** using Google Application Default Credentials (ADC).
3. **Maintain State** across multi-turn conversations using Conversation Tokens persisted to a local file.
4. **Handle Complex Tasks** by automatically resuming execution when the agent finishes with `DEADLINE_EXCEEDED`.
5. **Configure Extensions** like `Instruction` to customize agent behavior.

## Features

-   **Native A2A SDK Usage:** Uses `A2ACardResolver` and `create_client` for
    idiomatic protocol interaction.
-   **Streaming-only Execution:** Hardcoded to use response streaming for lowest
    real-time latency and optimal interaction patterns.
-   **Session Persistence:** Automatically saves and loads the
    `conversationToken` from a local file, allowing multi-turn conversations via
    repeated script executions.
-   **Configurable Parameters:** Exposes `gcp_resource_id` for flexibility,
    automatically extracting project and location details.
-   **Instruction Loading:** Automatically reads custom instructions from local
    files or directories, using filenames as the instruction name and file
    content as the definition.
-   **Extension Header Support:** Uses `ServiceParametersFactory` to correctly
    set the `A2A-Extensions` HTTP header required by the agent.
-   **Automated Resumption:** Detects `DEADLINE_EXCEEDED` via the
    `finish_reason` extension and transparently continues the task.

## Prerequisites

-   Python 3.10 or higher.
-   [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install)
    installed and configured.
-   Enable required APIs
    [Use the Data Engineering Agent to build and modify data pipelines](https://docs.cloud.google.com/bigquery/docs/data-engineering-agent-pipelines#required-apis)

## Setup

1.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .dea
    source .dea/bin/activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Authenticate with Google Cloud:**

    ```bash
    gcloud auth application-default login
    ```

## Usage

### Single Message Mode

Sends a single message and exits. `gcp_resource_id` and `message` are required.

```
python3 dea_a2a_client.py \
    --gcp_resource_id projects/my-project/locations/us-central1/repositories/my-repo/workspaces/default \
    --message "List my Dataform tables"
```

### Multi-turn Conversation (State Persistence)

To maintain a conversation across multiple calls, use the
`--conversation_token_path` argument. The script will save the conversation
token to this file and reload it in subsequent calls.

```
# First turn (starts session)
python3 dea_a2a_client.py \
    --gcp_resource_id projects/my-project/locations/us-central1/repositories/my-repo/workspaces/default \
    --message "hi" \
    --conversation_token_path ./token.txt

# Second turn (continues previous context)
python3 dea_a2a_client.py \
    --gcp_resource_id projects/my-project/locations/us-central1/repositories/my-repo/workspaces/default \
    --message "Explain the first table" \
    --conversation_token_path ./token.txt
```

### Advanced: Providing Local Instructions

You can point the client to local files (e.g., SQL style guides) to influence
the agent's behavior.

```
python3 dea_a2a_client.py \
    --gcp_resource_id projects/my-project/locations/us-central1/repositories/my-repo/workspaces/default \
    --message "List my tables" \
    --instruction_path ./style_guide.md
```

#### Command-line Arguments

Argument                    | Required | Description
:-------------------------- | :------- | :----------
`--gcp_resource_id`         | **Yes**  | The target Google Cloud resource ID. Supported formats `projects/{p}/locations/{l}/repositories/{r}/workspaces/{w}` (Dataform)
`--message`                 | **Yes**  | The message to send to the agent.
`--conversation_token_path` | No       | Path to a local file to persist conversation token. Allows for multi-turn conversations.
`--instruction_path`        | No       | Path to a file or directory containing instructions. Can be repeated.

### Running Unit Tests

Make sure the virtual environment is activated, then run:

```bash
python3 dea_a2a_client_test.py
```

Alternatively, if the virtual environment is not activated, you can run it
directly using the venv python:

```bash
./.dea/bin/python3 dea_a2a_client_test.py
```

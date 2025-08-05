# Cloud Run MCP Server Sample

This sample shows how to deploy a remote MCP server to Cloud Run.

This sample uses the `streamable-http` transport, which allows for running MCP
servers remotely. You can read more about MCP transports in the
[official MCP docs](https://modelcontextprotocol.io/docs/concepts/architecture#transport-layer).

## Benefits of running an MCP server remotely

Running an MCP server remotely on Cloud Run can provide several benefits:

- **📈 Scalability**: Cloud Run is built to [rapidly scale out to handle all incoming requests](https://cloud.google.com/run/docs/about-instance-autoscaling).
Cloud Run will scale your MCP server automatically based on demand.  
- **👥 Centralized server**: You can share access to a centralized MCP server
with team members through IAM privileges, allowing them to connect to it from
their local machines instead of all running their own servers locally. If a
change is made to the MCP server, all team members will benefit from it.  
- **🔐 Security**: Cloud Run provides an easy way to force authenticated
requests. This allows only secure connections to your MCP server, preventing
unauthorized access.

> [!IMPORTANT]
> The security aspect mentioned above is critical. If you don't enforce
authentication, anyone on the public internet can potentially access and
call your MCP server.

## Math MCP Server

LLMs are great at **non-deterministic tasks**: understanding intent, generating
creative text, summarizing complex ideas, and reasoning about abstract
concepts. However, they are notoriously unreliable for **deterministic tasks**
– things that have one, and only one, correct answer.

Enabling LLMs with **deterministic tools** (such as math operations) is one
example of how tools can provide valuable context to improve the use of LLMs
using MCP.

This sample uses [FastMCP](https://gofastmcp.com/getting-started/welcome) to create
a simple math MCP server that has two tools: `add` and `subtract`. FastMCP
provides a fast, Pythonic way to build MCP servers and clients.


## Prerequisites

- Python 3.10+
- Uv (for package and project management, see [docs for installation](https://docs.astral.sh/uv/getting-started/installation/))
- Google Cloud SDK (gcloud)

## Setup

Set your Google Cloud credentials and project.

```bash
gcloud auth login
export PROJECT_ID=<your-project-id>
gcloud config set project $PROJECT_ID
```

## Deploy

You can deploy directly from source or using a container image.

Both options use the `--no-allow-unauthenticated` flag to require authentication.

This is important for security reasons. If you don't require authentication,
anyone can call your MCP server and potentially cause damage to your system.

<details open>
<summary>Option 1 - Deploy from source</summary>

```bash
gcloud run deploy mcp-server --no-allow-unauthenticated --region=us-central1 --source .
```

</details>

<details>
<summary>Option 2 - Deploy from a container image</summary>

Create an Artifact Registry repository to store the container image.

```bash
gcloud artifacts repositories create mcp-servers \
  --repository-format=docker \
  --location=us-central1 \
  --description="Repository for remote MCP servers" \
  --project=$PROJECT_ID
```

Build the container image and push it to Artifact Registry with Cloud Build.

```bash
gcloud builds submit --region=us-central1 --tag us-central1-docker.pkg.dev/$PROJECT_ID/mcp-servers/mcp-server:latest
```

Deploy the container image to Cloud Run.

```bash
gcloud run deploy mcp-server \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/mcp-servers/mcp-server:latest \
  --region=us-central1 \
  --no-allow-unauthenticated
```

</details>

If your service has successfully deployed you will see a message like the following:

```bash
Service [mcp-server] revision [mcp-server-12345-abc] has been deployed and is serving 100 percent of traffic.
```

## Authenticating MCP Clients

Since you specified `--no-allow-unauthenticated` to require authentication, any
MCP client connecting to the remote MCP server will need to authenticate.

The official docs for [Host MCP servers on Cloud Run](https://cloud.google.com/run/docs/host-mcp-servers#authenticate_mcp_clients)
provides more information on this topic depending on where the MCP client is
running.

For this sample, run the [Cloud Run proxy](https://cloud.google.com/sdk/gcloud/reference/run/services/proxy)
to create an authenticated tunnel to the remote MCP server on your local
machine.

By default, the URL of Cloud Run service requires all requests to be
authorized with the [Cloud Run Invoker](https://cloud.google.com/run/docs/securing/managing-access#invoker)
(`roles/run.invoker`) IAM role. This IAM policy binding ensures that a
strong security mechanism is used to authenticate your local MCP client.

You should make sure that you or any team members trying to access the remote
MCP server have the `roles/run.invoker` IAM role bound to their Google Cloud
account.

> [!TIP] 
> The below command may prompt you to download the Cloud Run proxy if it is
> not already installed. Follow the prompts to download and install it.

```bash
gcloud run services proxy mcp-server --region=us-central1
```

You should see the following output:

```bash
Proxying to Cloud Run service [mcp-server] in project [<YOUR_PROJECT_ID>] region [us-central1]
http://127.0.0.1:8080 proxies to https://mcp-server-abcdefgh-uc.a.run.app
```

All traffic to `http://127.0.0.1:8080` will now be authenticated and forwarded to
the remote MCP server.

## Testing the remote MCP server

To test the remote MCP server use the
[test_server.py](test_server.py) test script. It uses the FastMCP client to
connect to `http://127.0.0.1:8080/mcp` (note the `/mcp` at the end for the
`streamable-http` transport) and calls the `add` and `subtract` tools.

> [!NOTE]
> Make sure you have the Cloud Run proxy running before running the test server.

In a **new terminal** run:

```bash
uv run test_server.py
```

You should see the following output:

```bash
>>> 🛠️  Tool found: add
>>> 🛠️  Tool found: subtract
>>> 🪛  Calling add tool for 1 + 2
<<< ✅ Result: 3
>>> 🪛  Calling subtract tool for 10 - 3
<<< ✅ Result: 7
```

You have successfully deployed a remote MCP server to Cloud Run and tested it
using the FastMCP client.

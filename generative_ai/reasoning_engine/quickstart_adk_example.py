import vertexai
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

# [START agentengine_quickstart_adk_tool]
def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
) -> dict:
    """Retrieves the exchange rate between two currencies on a specified date."""
    import requests

    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()
# [END agentengine_quickstart_adk_tool]

async def quickstart_adk_example(staging_bucket: str) -> list:

    # [START agentengine_quickstart_adk_agent_init]
    from google.adk.agents import Agent
    from vertexai import agent_engines
    
    agent = Agent(
        model="gemini-2.0-flash",
        name="currency_exchange_agent",
        tools=[get_exchange_rate],
    )
    
    app = agent_engines.AdkApp(agent=agent)
    # [END agentengine_quickstart_adk_agent_init]

    # [START agentengine_quickstart_adk_testlocally]
    async for event in app.async_stream_query(
        user_id="USER_ID",
        message="What is the exchange rate from US dollars to SEK today?",
    ):
        print(event)
    # [END agentengine_quickstart_adk_testlocally]

    # [START agentengine_quickstart_adk_deploy]
    remote_agent = client.agent_engines.create(
        agent=app,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
            "staging_bucket": staging_bucket,
        }
    )
    # [END agentengine_quickstart_adk_deploy]

    events = []
    # [START agentengine_quickstart_adk_testremotely]
    async for event in remote_agent.async_stream_query(
        user_id="USER_ID",
        message="What is the exchange rate from US dollars to SEK today?",
    ):
        print(event)
        events.append(event)
    # [END agentengine_quickstart_adk_testremotely]
    
    remote_agent.delete(force=True)
    return events

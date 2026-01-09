import vertexai
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date."""
    import requests

    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()

def quickstart_adk_example(staging_bucket: str) -> reasoning_engines.ReasoningEngine:

    from google.adk.agents import Agent
    from vertexai import agent_engines
    
    agent = Agent(
        model="gemini-2.0-flash",
        name='currency_exchange_agent',
        tools=[get_exchange_rate],
    )
    
    app = agent_engines.AdkApp(agent=agent)
    
    async for event in app.async_stream_query(
        user_id="USER_ID",
        message="What is the exchange rate from US dollars to SEK today?",
    ):
        print(event)
    
    remote_agent = client.agent_engines.create(
        agent=app,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
            "staging_bucket": "STAGING_BUCKET",
        }
    )

    events = []
    async for event in remote_agent.async_stream_query(
        user_id="USER_ID",
        message="What is the exchange rate from US dollars to SEK today?",
    ):
        print(event)
        events.append(event)
    
    remote_agent.delete(force=True)
    return events

# Copyright 2024 Google LLC
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
import os

from typing import Dict, Union

from vertexai.preview import reasoning_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_reasoning_engine_advanced(
    staging_bucket: str,
) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_create_reasoning_engine_advanced]

    from typing import List

    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # staging_bucket = "gs://YOUR_BUCKET_NAME"

    vertexai.init(
        project=PROJECT_ID, location="us-central1", staging_bucket=staging_bucket
    )

    class LangchainApp:
        def __init__(self, project: str, location: str) -> None:
            self.project_id = project
            self.location = location

        def set_up(self) -> None:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_google_vertexai import ChatVertexAI

            system = (
                "You are a helpful assistant that answers questions "
                "about Google Cloud."
            )
            human = "{text}"
            prompt = ChatPromptTemplate.from_messages(
                [("system", system), ("human", human)]
            )
            chat = ChatVertexAI(project=self.project_id, location=self.location)
            self.chain = prompt | chat

        def query(self, question: str) -> Union[str, List[Union[str, Dict]]]:
            """Query the application.
            Args:
                question: The user prompt.
            Returns:
                str: The LLM response.
            """
            return self.chain.invoke({"text": question}).content

    # Locally test
    app = LangchainApp(project=PROJECT_ID, location="us-central1")
    app.set_up()
    print(app.query("What is Vertex AI?"))

    # Create a remote app with Reasoning Engine
    # Deployment of the app should take a few minutes to complete.
    reasoning_engine = reasoning_engines.ReasoningEngine.create(
        LangchainApp(project=PROJECT_ID, location="us-central1"),
        requirements=[
            "google-cloud-aiplatform[langchain,reasoningengine]",
            "cloudpickle==3.0.0",
            "pydantic==2.7.4",
        ],
        display_name="Demo LangChain App",
        description="This is a simple LangChain app.",
        # sys_version="3.10",  # Optional
        extra_packages=[],
    )
    # Example response:
    # Model_name will become a required arg for VertexAIEmbeddings starting...
    # ...
    # Create ReasoningEngine backing LRO: projects/123456789/locations/us-central1/reasoningEngines/...
    # ReasoningEngine created. Resource name: projects/123456789/locations/us-central1/reasoningEngines/...
    # ...

    # [END generativeaionvertexai_create_reasoning_engine_advanced]
    return reasoning_engine


if __name__ == "__main__":
    create_reasoning_engine_advanced("gs://your-bucket-unique-name")

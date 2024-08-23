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

from typing import Dict, List, Union

from vertexai.preview import reasoning_engines


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_reasoning_engine_basic(
    staging_bucket: str,
) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_create_reasoning_engine_basic]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update project and staging_bucket
    # PROJECT_ID = "your-project-id"
    # staging_bucket = "gs://YOUR_BUCKET_NAME"
    vertexai.init(
        project=PROJECT_ID, location="us-central1", staging_bucket=staging_bucket
    )

    class SimpleAdditionApp:
        def query(self, a: int, b: int) -> str:
            """Query the application.
            Args:
                a: The first input number
                b: The second input number
            Returns:
                int: The additional result.
            """
            return f"{int(a)} + {int(b)} is {int(a + b)}"

    # Locally test
    app = SimpleAdditionApp()
    app.query(a=1, b=2)

    # Create a remote app with reasoning engine.
    # This may take 1-2 minutes to finish.
    reasoning_engine = reasoning_engines.ReasoningEngine.create(
        SimpleAdditionApp(),
        display_name="Demo Addition App",
        description="A simple demo addition app",
        requirements=["cloudpickle==3"],
        extra_packages=[],
    )
    # [END generativeaionvertexai_create_reasoning_engine_basic]
    return reasoning_engine


def create_reasoning_engine_advanced(
    staging_bucket: str,
) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_create_reasoning_engine_advanced]

    from typing import List

    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update project_id and staging_bucket
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

    # Create a remote app with reasoning engine
    # This may take 1-2 minutes to finish because it builds a container and turn up HTTP servers.
    reasoning_engine = reasoning_engines.ReasoningEngine.create(
        LangchainApp(project=PROJECT_ID, location="us-central1"),
        requirements=[
            "google-cloud-aiplatform==1.50.0",
            "langchain-google-vertexai",
            "langchain-core",
            "cloudpickle==3",
        ],
        display_name="Demo LangChain App",
        description="This is a simple LangChain app.",
        # sys_version="3.10",  # Optional
        extra_packages=[],
    )
    # [END generativeaionvertexai_create_reasoning_engine_advanced]
    return reasoning_engine


def query_reasoning_engine(reasoning_engine_id: str) -> object:
    # [START generativeaionvertexai_query_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update project id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")
    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)

    # Replace with kwargs for `.query()` method.
    response = reasoning_engine.query(a=1, b=2)
    print(response)
    # [END generativeaionvertexai_query_reasoning_engine]
    return response


def list_reasoning_engines() -> List[reasoning_engines.ReasoningEngine]:
    # [START generativeaionvertexai_list_reasoning_engines]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update project_id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reasoning_engine_list = reasoning_engines.ReasoningEngine.list()
    print(reasoning_engine_list)
    # [END generativeaionvertexai_list_reasoning_engines]
    return reasoning_engine_list


def get_reasoning_engine(reasoning_engine_id: str) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_get_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update project_id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)
    print(reasoning_engine)
    # [END generativeaionvertexai_get_reasoning_engine]
    return reasoning_engine


def delete_reasoning_engine(reasoning_engine_id: str) -> None:
    # [START generativeaionvertexai_delete_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update project_id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)
    reasoning_engine.delete()
    # [END generativeaionvertexai_delete_reasoning_engine]

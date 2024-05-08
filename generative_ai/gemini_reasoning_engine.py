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

from typing import List

from vertexai.preview import reasoning_engines


def create_reasoning_engine_basic(project_id: str) -> reasoning_engines.ReasoningEngine:

    # [START generativeaionvertexai_create_reasoning_engine_basic]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    class SimpleAdditionApp:
        def query(self, a: int, b: int):
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
        requirements=[],
        extra_packages=[],
    )
    # [END generativeaionvertexai_create_reasoning_engine_basic]
    return reasoning_engine


def create_reasoning_engine_advanced(
    project_id: str, location: str
) -> reasoning_engines.ReasoningEngine:

    # [START generativeaionvertexai_create_reasoning_engine_advanced]

    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"

    class LangchainApp:
        def __init__(self, project: str, location: str):
            self.project_id = project
            self.location = location

        def set_up(self):
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

        def query(self, question: str):
            """Query the application.

            Args:
                question: The user prompt.

            Returns:
                str: The LLM response.
            """
            return self.chain.invoke({"text": question}).content

    # Locally test
    app = LangchainApp(project=project_id, location=location)
    app.set_up()
    print(app.query("What is Vertex AI?"))

    vertexai.init(project=project_id, location=location)

    # Create a remote app with reasoning engine
    # This may take 1-2 minutes to finish because it builds a container and turn up HTTP servers.
    reasoning_engine = reasoning_engines.ReasoningEngine.create(
        LangchainApp(project=project_id, location=location),
        requirements=[
            "google-cloud-aiplatform==1.50.0",
            "langchain-google-vertexai",
            "langchain-core",
        ],
        display_name="Demo LangChain App",
        description="This is a simple LangChain app.",
        sys_version="3.10",
        extra_packages=[],
    )
    # [END generativeaionvertexai_create_reasoning_engine_advanced]
    return reasoning_engine


def query_reasoning_engine(project_id: str, reasoning_engine_id: str) -> object:
    # [START generativeaionvertexai_query_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # reasoning_engine_id = "REASONING_ENGINE_ID"

    vertexai.init(project=project_id, location="us-central1")
    remote_app = reasoning_engines.ReasoningEngine(reasoning_engine_id)

    # Replace with kwargs for `.query()` method.
    response = remote_app.query(question="What is Vertex AI?")
    print(response)
    # [END generativeaionvertexai_query_reasoning_engine]
    return response


def list_reasoning_engines(project_id: str) -> List[reasoning_engines.ReasoningEngine]:
    # [START generativeaionvertexai_list_reasoning_engines]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    reasoning_engine_list = reasoning_engines.ReasoningEngine.list()
    print(reasoning_engine_list)
    # [END generativeaionvertexai_list_reasoning_engines]
    return reasoning_engine_list


def get_reasoning_engine(
    project_id: str, reasoning_engine_id: str
) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_get_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # reasoning_engine_id = "REASONING_ENGINE_ID"

    vertexai.init(project=project_id, location="us-central1")

    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)
    print(reasoning_engine)
    # [END generativeaionvertexai_get_reasoning_engine]
    return reasoning_engine


def delete_reasoning_engine(project_id: str, reasoning_engine_id: str) -> None:
    # [START generativeaionvertexai_delete_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # reasoning_engine_id = "REASONING_ENGINE_ID"

    vertexai.init(project=project_id, location="us-central1")

    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)
    reasoning_engine.delete()
    # [END generativeaionvertexai_delete_reasoning_engine]

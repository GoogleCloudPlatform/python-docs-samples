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

from vertexai.preview import reasoning_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_reasoning_engine_basic(
    staging_bucket: str,
) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_create_reasoning_engine_basic]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
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

    # Create a remote app with Reasoning Engine.
    # This may take 1-2 minutes to finish.
    reasoning_engine = reasoning_engines.ReasoningEngine.create(
        SimpleAdditionApp(),
        display_name="Demo Addition App",
        description="A simple demo addition app",
        requirements=["cloudpickle==3"],
        extra_packages=[],
    )
    # Example response:
    # Using bucket YOUR_BUCKET_NAME
    # Writing to gs://YOUR_BUCKET_NAME/reasoning_engine/reasoning_engine.pkl
    # ...
    # ReasoningEngine created. Resource name: projects/123456789/locations/us-central1/reasoningEngines/123456
    # To use this ReasoningEngine in another session:
    # reasoning_engine = vertexai.preview.reasoning_engines.ReasoningEngine('projects/123456789/locations/...

    # [END generativeaionvertexai_create_reasoning_engine_basic]
    return reasoning_engine


if __name__ == "__main__":
    create_reasoning_engine_basic("gs://your-bucket-unique-name")

# Copyright 2025 Google LLC
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


def get_bearer_token() -> str:
    """To get project name and bearer token for Google Cloud ADC authentication."""
    import google.auth
    from google.auth.transport.requests import Request

    creds, project_name = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = Request()
    creds.refresh(auth_req)
    bearer_token = creds.token
    return project_name, bearer_token


def generate_content() -> str:
    """To generate content from DeepSeek model hosted in Vertex AI Model Garden."""
    import requests
    import json

    project_name, bearer_token = get_bearer_token()

    # Read more about the model here:
    #   https://cloud.google.com/vertex-ai/generative-ai/docs/maas/deepseek#streaming
    location = "us-central1"
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_name}/locations/{location}/endpoints/openapi/chat/completions"

    # Set the request header
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-ai/deepseek-r1-0528-maas",
        # "stream": False,  # As per the bash script
        "messages": [{"role": "user", "content": "Why is the sky blue?"}],
    }
    # Send the request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Request Response: {response.status_code}")
    # Example response:
    #   Request Response: 200

    # Load the response data
    model_response = json.loads(response.content)
    print(model_response["model"])
    # Example response:
    #   'deepseek-ai/deepseek-r1-0528-maas'
    print(model_response["usage"])
    # Example response:
    #   {
    #   'completion_tokens': 3294,
    #   'prompt_tokens': 10,
    #   'total_tokens': 3304
    #   }

    # Print user input & Model response
    for each in data["messages"]:
        print(f"{each['role']}>>> {each['content']}")
    for each in model_response["choices"]:
        print(f"{each['message']['role']}>>> {each['message']['content']}")
    # Example response:
    #  user>>> Why is the sky blue?
    # Example response:
    #  assistant>>> <think>
    #               Okay, the user is asking why the sky is blue.
    #               ...
    #               </think>

    #               The sky appears blue due to a phenomenon called **Rayleigh scattering**,
    #               which occurs when sunlight passes through Earth's atmosphere and
    #              ...
    return response.content


if __name__ == "__main__":
    generate_content()

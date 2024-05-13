# Copyright 2024 shihc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

vertexai.init(project="project-id", location="us-west1")
model = GenerativeModel("gemini-1.0-pro")

prompt_template: str = """/
You are a personal assistant. Please give responses to the following question: {question}./
Do not use technical words, give easy to understand responses.
"""

def start_chat(question: str):
    prompt = prompt_template.replace("{question}", question)
    chat = model.start_chat()
    responses = chat.send_message(prompt, stream=True)
    for response in responses:
        print(response.text, end="")

if __name__ == '__main__':
    start_chat("Why the sky is blue?")
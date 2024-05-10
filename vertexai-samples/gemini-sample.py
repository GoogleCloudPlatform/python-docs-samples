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
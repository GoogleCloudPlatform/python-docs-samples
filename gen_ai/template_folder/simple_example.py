# # Copyright 2024 Google LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #    https://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
#
#
# def simple_example() -> int:
#     "Simple example for <template_folder> feature."
#     # TODO: <ADD-START-REGION-TAG-HERE>
#     from vertexai.preview.tokenization import get_tokenizer_for_model
#
#     # Using local tokenzier
#     tokenizer = get_tokenizer_for_model("gemini-1.5-flash-002")
#
#     prompt = "hello world"
#     response = tokenizer.count_tokens(prompt)
#     print(f"Prompt Token Count: {response.total_tokens}")
#     # Example response:
#     # Prompt Token Count: 2
#
#     prompt = ["hello world", "what's the weather today"]
#     response = tokenizer.count_tokens(prompt)
#     print(f"Prompt Token Count: {response.total_tokens}")
#     # Example response:
#     # Prompt Token Count: 8
#
#     # TODO: <ADD-START-REGION-TAG-HERE>
#     return response.total_tokens
#
#
# if __name__ == "__main__":
#     simple_example()

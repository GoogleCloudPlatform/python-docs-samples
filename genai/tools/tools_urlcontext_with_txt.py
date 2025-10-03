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


def generate_content() -> str:
    # [START googlegenaisdk_tools_urlcontext_with_txt]
    from google import genai
    from google.genai.types import Tool, GenerateContentConfig, HttpOptions, UrlContext

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.5-flash"

    url_context_tool = Tool(
        url_context=UrlContext
    )

    #todo(developer) Here put your URLs
    url1 = ""
    url2 = ""

    response = client.models.generate_content(
        model=model_id,
        contents=f"Compare recipes from {url1} and {url2}",
        config=GenerateContentConfig(
            tools=[url_context_tool],
            response_modalities=["TEXT"],
        )
    )

    for each in response.candidates[0].content.parts:
        print(each.text)
    # get URLs retrieved for context
    print(response.candidates[0].url_context_metadata)
    # [END googlegenaisdk_tools_urlcontext_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()

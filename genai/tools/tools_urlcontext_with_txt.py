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

    # TODO(developer): Here put your URLs
    url1 = "https://cloud.google.com/vertex-ai/docs/generative-ai/start"
    url2 = "https://cloud.google.com/docs/overview"

    response = client.models.generate_content(
        model=model_id,
        contents=f"Compare the content, purpose, and audiences of {url1} and {url2}.",
        config=GenerateContentConfig(
            tools=[url_context_tool],
            response_modalities=["TEXT"],
        )
    )

    for each in response.candidates[0].content.parts:
        print(each.text)
    # Gemini 2.5 Pro and Gemini 2.5 Flash are both advanced models offered by Google AI, but they are optimized for different use cases.
    #
    # Here's a comparison:
    #
    # **Gemini 2.5 Pro**
    # *   **Description**: This is Google's most advanced model, described as a "state-of-the-art thinking model". It excels at reasoning over complex problems in areas like code, mathematics, and STEM, and can analyze large datasets, codebases, and documents using a long context window.
    # *   **Input Data Types**: It supports audio, images, video, text, and PDF inputs.
    # *   **Output Data Types**: It produces text outputs.
    # *   **Token Limits**: It has an input token limit of 1,048,576 and an output token limit of 65,536.
    # *   **Supported Capabilities**: Gemini 2.5 Pro supports Batch API, Caching, Code execution, Function calling, Search grounding, Structured outputs, Thinking, and URL context.
    # *   **Knowledge Cutoff**: January 2025.
    #
    # **Gemini 2.5 Flash**
    # *   **Description**: Positioned as "fast and intelligent," Gemini 2.5 Flash is highlighted as Google's best model in terms of price-performance, offering well-rounded capabilities. It is ideal for large-scale processing, low-latency, high-volume tasks that require thinking, and agentic use cases.
    # *   **Input Data Types**: It supports text, images, video, and audio inputs.
    # *   **Output Data Types**: It produces text outputs.
    # *   **Token Limits**: Similar to Pro, it has an input token limit of 1,048,576 and an output token limit of 65,536.
    # *   **Supported Capabilities**: Gemini 2.5 Flash supports Batch API, Caching, Code execution, Function calling, Search grounding, Structured outputs, Thinking, and URL context.
    # *   **Knowledge Cutoff**: January 2025.
    #
    # **Key Differences and Similarities:**
    #
    # *   **Primary Focus**: Gemini 2.5 Pro is geared towards advanced reasoning and in-depth analysis of complex problems and large documents. Gemini 2.5 Flash, on the other hand, is optimized for efficiency, scale, and high-volume, low-latency applications, making it a strong choice for price-performance sensitive scenarios.
    # *   **Input Modalities**: Both models handle various input types including text, images, video, and audio. Gemini 2.5 Pro explicitly lists PDF as an input type, while Gemini 2.5 Flash lists text, images, video, audio.
    # *   **Technical Specifications (for primary stable versions)**: Both models share the same substantial input and output token limits (1,048,576 input and 65,536 output). They also support a very similar set of core capabilities, including code execution, function calling, and URL context. Neither model supports audio generation, image generation, or Live API in their standard stable versions.
    # *   **Knowledge Cutoff**: Both models have a knowledge cutoff of January 2025.
    #
    # In essence, while both models are powerful and capable, Gemini 2.5 Pro is designed for maximum performance in complex reasoning tasks, whereas Gemini 2.5 Flash prioritizes cost-effectiveness and speed for broader, high-throughput applications.
    # get URLs retrieved for context
    print(response.candidates[0].url_context_metadata)
    # url_metadata=[UrlMetadata(
    #   retrieved_url='https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash',
    #   url_retrieval_status=<UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS: 'URL_RETRIEVAL_STATUS_SUCCESS'>
    # ), UrlMetadata(
    #   retrieved_url='https://ai.google.dev/gemini-api/docs/models#gemini-2.5-pro',
    #   url_retrieval_status=<UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS: 'URL_RETRIEVAL_STATUS_SUCCESS'>
    # )]
    # [END googlegenaisdk_tools_urlcontext_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()

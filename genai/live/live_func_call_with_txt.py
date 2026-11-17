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

import asyncio

from google.genai.types import FunctionResponse


async def generate_content() -> list[FunctionResponse]:
    # [START googlegenaisdk_live_func_call_with_txt]
    from google import genai
    from google.genai.types import (
        AudioTranscriptionConfig,
        Content,
        FunctionDeclaration,
        FunctionResponse,
        LiveConnectConfig,
        Modality,
        Part,
        Tool,
    )

    client = genai.Client()
    model_id = "gemini-3.8-live"

    # Simple function definitions
    turn_on_the_lights = FunctionDeclaration(name="turn_on_the_lights")
    turn_off_the_lights = FunctionDeclaration(name="turn_off_the_lights")

    config = LiveConnectConfig(
        response_modalities=[Modality.AUDIO],
        output_audio_transcription=AudioTranscriptionConfig(),
        tools=[Tool(function_declarations=[turn_on_the_lights, turn_off_the_lights])],
    )
    async with client.aio.live.connect(model=model_id, config=config) as session:
        text_input = "Turn on the lights please"
        print("> ", text_input, "\n")
        await session.send_client_content(
            turns=Content(role="user", parts=[Part(text=text_input)])
        )

        function_responses = []

        # The first turn ends after the model requests the function calls.
        async for chunk in session.receive():
            if chunk.tool_call:
                for fc in chunk.tool_call.function_calls:
                    function_response = FunctionResponse(
                        id=fc.id,
                        name=fc.name,
                        response={
                            "result": "ok"
                        },  # simple, hard-coded function response
                    )
                    function_responses.append(function_response)
                    print(f"{fc.name}: {function_response.response['result']}")

                await session.send_tool_response(function_responses=function_responses)

        # The next turn contains the model's answer, which uses the function results.
        response = []
        async for chunk in session.receive():
            server_content = chunk.server_content
            if server_content and server_content.output_transcription:
                if server_content.output_transcription.text:
                    response.append(server_content.output_transcription.text)
        print("".join(response))

    # Example output:
    # >  Turn on the lights please
    # turn_on_the_lights: ok
    # I've turned on the lights for you.
    # [END googlegenaisdk_live_func_call_with_txt]
    return True


if __name__ == "__main__":
    asyncio.run(generate_content())

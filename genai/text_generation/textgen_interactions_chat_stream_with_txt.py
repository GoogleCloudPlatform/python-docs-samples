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


def create_interaction() -> bool:
    # [START googlegenaisdk_interactions_textgen_chat_stream_with_txt]
    from google import genai

    client = genai.Client()

    interaction1 = client.interactions.create(
        model="gemini-3.8-flash",
        input="Hello",
    )

    stream = client.interactions.create(
        model="gemini-3.8-flash",
        previous_interaction_id=interaction1.id,
        input="Why is the sky blue?",
        stream=True,
    )

    for event in stream:
        if event.event_type == "step.delta" and event.delta:
            if getattr(event.delta, "type", None) == "text" and getattr(
                event.delta, "text", None
            ):
                print(event.delta.text, end="", flush=True)
    # Example response:
    # The
    #  sky appears blue due to a phenomenon called **Rayleigh scattering**. Here's
    #  a breakdown of why:
    # ...
    # [END googlegenaisdk_interactions_textgen_chat_stream_with_txt]
    return True


if __name__ == "__main__":
    create_interaction()

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_helloworld_gradio]
import gradio as gr

def hello(name, intensity):
    """Return a friendly greeting."""
    return "Hello " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=hello,
    inputs=["text", "slider"],
    outputs=["text"],
    title="Hello World 👋🌎",
    description=("Type your name below and hit 'Submit', and try the slider to "
                 "make the greeting louder!"),
    theme="soft",
    flagging_mode="never",
)

demo.launch()
# [END cloudrun_helloworld_gradio]

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

from streamlit.testing.v1 import AppTest

def test_balloons():
    """A user presses the balloons button"""
    at = AppTest.from_file("main.py").run()
    at.text_input[0].set_value("Foo").run()
    at.button[0].click().run()
    assert at.markdown.values[0] == "This is a demo Streamlit app.\n\nEnter your name in the text box below and press a button to see some fun features in Streamlit."
    assert at.markdown.values[1] == "Time to celebrate Foo! 🥳"
    assert at.markdown.values[2] == "You deployed a Streamlit app! 👏"

def test_snow():
    """A user presses the snow button"""
    at = AppTest.from_file("main.py").run()
    at.text_input[0].set_value("Foo").run()
    at.button[1].click().run()
    assert at.markdown.values[0] == "This is a demo Streamlit app.\n\nEnter your name in the text box below and press a button to see some fun features in Streamlit."
    assert at.markdown.values[1] == "Let it snow Foo! 🌨️"
    assert at.markdown.values[2] == "You deployed a Streamlit app! 👏"
    

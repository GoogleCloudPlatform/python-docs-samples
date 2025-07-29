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

# [START cloudrun_helloworld_streamlit]
import streamlit as st

st.title(f"Hello World! 👋🌎")
st.markdown(
    """
    This is a demo Streamlit app.

    Enter your name in the text box below and press a button to see some fun features in Streamlit.
    """
)

name = st.text_input("Enter your name:")

# Use columns to create buttons side by side
col1, col2 = st.columns(2)

with col1:
    if st.button("Send balloons! 🎈"):
        st.balloons()
        st.write(f"Time to celebrate {name}! 🥳")
        st.write("You deployed a Streamlit app! 👏")

with col2:
    if st.button("Send snow! ❄️"):
        st.snow()
        st.write(f"Let it snow {name}! 🌨️")
        st.write("You deployed a Streamlit app! 👏")
# [END cloudrun_helloworld_streamlit]

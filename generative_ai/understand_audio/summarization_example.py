# Copyright 2024 Google LLC
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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def summarize_audio() -> str:
    """Summarizes the content of an audio file using a pre-trained generative model."""
    # [START generativeaionvertexai_gemini_audio_summarization]

    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = """
    Please provide a summary for the audio.
    Provide chapter titles, be concise and short, no need to provide chapter summaries.
    Do not make up any information that is not part of the audio and do not be verbose.
    """

    audio_file_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = model.generate_content(contents)
    print(response.text)
    # Example response:
    # **Made By Google Podcast Summary**
    # **Chapter Titles:**
    # * Introduction
    # * Transformative Pixel Features
    # ...

    # [END generativeaionvertexai_gemini_audio_summarization]
    return response.text


if __name__ == "__main__":
    summarize_audio()

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


def summarize_audio(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_audio_summarization]

    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    prompt = """
    Please provide a summary for the audio.
    Provide chapter titles with timestamps, be concise and short, no need to provide chapter summaries.
    Do not make up any information that is not part of the audio and do not be verbose.
  """

    audio_file_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = model.generate_content(contents)
    print(response.text)

    # [END generativeaionvertexai_gemini_audio_summarization]
    return response.text


def transcript_audio(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_audio_transcription]

    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    prompt = """
    Can you transcribe this interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
  """

    audio_file_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = model.generate_content(contents)
    print(response.text)

    # [END generativeaionvertexai_gemini_audio_transcription]
    return response.text

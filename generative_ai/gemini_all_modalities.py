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


def analyze_all_modalities(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_all_modalities]

    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    video_file_uri = (
        "gs://cloud-samples-data/generative-ai/video/behind_the_scenes_pixel.mp4"
    )
    video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")

    image_file_uri = "gs://cloud-samples-data/generative-ai/image/a-man-and-a-dog.png"
    image_file = Part.from_uri(image_file_uri, mime_type="image/png")

    prompt = """
    Watch each frame in the video carefully and answer the questions.
    Only base your answers strictly on what information is available in the video attached.
    Do not make up any information that is not part of the video and do not be too
    verbose, be to the point.

    Questions:
    - When is the moment in the image happening in the video? Provide a timestamp.
    - What is the context of the moment and what does the narrator say about it?
  """

    contents = [
        video_file,
        image_file,
        prompt,
    ]

    response = model.generate_content(contents)
    print(response.text)

    # [END generativeaionvertexai_gemini_all_modalities]
    return response.text

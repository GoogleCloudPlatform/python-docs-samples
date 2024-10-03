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


def generate_content() -> str:
    # [START generativeaionvertexai_gemini_youtube_video_key_moments]
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO (developer): update project id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    contents = [
        # Text prompt
        "Identify the key moments of this video.",
        # YouTube video of Paris 2024 Olympics
        Part.from_uri("https://www.youtube.com/watch?v=6F5gZWcpNU4", "video/mp4"),
    ]

    response = model.generate_content(contents)
    print(response.text)
    # Example response
    #    This video is a fast-paced, exciting montage of athletes competing in and celebrating their victories in the 2024 Summer Olympics in Paris, France. Key moments include:
    #    - [00:00:01] The Olympic rings are shown with laser lights and fireworks in the opening ceremonies.
    #    - [00:00:02–00:00:08] Various shots of the games’ venues are shown, including aerial views of skateboarding and volleyball venues, a view of the track and field stadium, and a shot of the Palace of Versailles.
    #    - [00:00:09–00:01:16] A fast-paced montage shows highlights from various Olympic competitions.
    #    - [00:01:17–00:01:29] The video switches to show athletes celebrating victories, both tears of joy and tears of sadness are shown.
    #    - [00:01:30–00:02:26] The montage then continues to showcase sporting events, including cycling, kayaking, swimming, track and field, gymnastics, surfing, basketball, and ping-pong.
    #    - [00:02:27–00:04:03] More athletes celebrate their wins.
    #    - [00:04:04–00:04:55] More Olympic sports are shown, followed by more celebrations.
    #    - [00:04:56] Olympic medals are shown.
    #    - [00:04:57] An aerial shot of the Eiffel Tower lit up with the Olympic rings is shown at night.
    #    - [00:04:58–00:05:05] The video ends with a black screen and the words, “Sport. And More Than Sport.” written beneath the Olympic rings.
    # [END generativeaionvertexai_gemini_youtube_video_key_moments]
    return response.text


if __name__ == "__main__":
    generate_content()

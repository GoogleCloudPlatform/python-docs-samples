# Copyright 2023 Google LLC
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


def sentiment_analysis(
    temperature: float,
    project_id: str,
    location: str,
) -> str:
    """Sentiment analysis example with a Large Language Model."""
    # [START aiplatform_sdk_sentiment_analysis]
    import vertexai

    from vertexai.language_models import TextGenerationModel

    # TODO(developer): update project_id, location & temperature
    vertexai.init(project=project_id, location=location)
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 5,  # Token limit determines the maximum amount of text output.
        "top_p": 0,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 1,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        """I had to compare two versions of Hamlet for my Shakespeare class and \
unfortunately I picked this version. Everything from the acting (the actors \
deliver most of their lines directly to the camera) to the camera shots (all \
medium or close up shots...no scenery shots and very little back ground in the \
shots) were absolutely terrible. I watched this over my spring break and it is \
very safe to say that I feel that I was gypped out of 114 minutes of my \
vacation. Not recommended by any stretch of the imagination.
Classify the sentiment of the message: negative

Something surprised me about this movie - it was actually original. It was not \
the same old recycled crap that comes out of Hollywood every month. I saw this \
movie on video because I did not even know about it before I saw it at my \
local video store. If you see this movie available - rent it - you will not \
regret it.
Classify the sentiment of the message: positive

My family has watched Arthur Bach stumble and stammer since the movie first \
came out. We have most lines memorized. I watched it two weeks ago and still \
get tickled at the simple humor and view-at-life that Dudley Moore portrays. \
Liza Minelli did a wonderful job as the side kick - though I\'m not her \
biggest fan. This movie makes me just enjoy watching movies. My favorite scene \
is when Arthur is visiting his fiancée\'s house. His conversation with the \
butler and Susan\'s father is side-spitting. The line from the butler, \
"Would you care to wait in the Library" followed by Arthur\'s reply, \
"Yes I would, the bathroom is out of the question", is my NEWMAIL \
notification on my computer.
Classify the sentiment of the message: positive

This Charles outing is decent but this is a pretty low-key performance. Marlon \
Brando stands out. There\'s a subplot with Mira Sorvino and Donald Sutherland \
that forgets to develop and it hurts the film a little. I\'m still trying to \
figure out why Charlie want to change his name.
Classify the sentiment of the message: negative

Tweet: The Pixel 7 Pro, is too big to fit in my jeans pocket, so I bought \
new jeans.
Classify the sentiment of the message: """,
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    # [END aiplatform_sdk_sentiment_analysis]

    return response.text


if __name__ == "__main__":
    sentiment_analysis()

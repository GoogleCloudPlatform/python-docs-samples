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

# [START generativeai_sdk_extraction]
from vertex_ai.preview.language_models import TextGenerationModel


def extractive_question_answering(temperature=0):
    """Extractive Question Answering with a Large Language Model."""
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
      '''Background: There is evidence that there have been significant changes \
in Amazon rainforest vegetation over the last 21,000 years through the Last \
Glacial Maximum (LGM) and subsequent deglaciation. Analyses of sediment \
deposits from Amazon basin paleo lakes and from the Amazon Fan indicate that \
rainfall in the basin during the LGM was lower than for the present, and this \
was almost certainly associated with reduced moist tropical vegetation cover \
in the basin. There is debate, however, over how extensive this reduction \
was. Some scientists argue that the rainforest was reduced to small, isolated \
refugia separated by open forest and grassland; other scientists argue that \
the rainforest remained largely intact but extended less far to the north, \
south, and east than is seen today. This debate has proved difficult to \
resolve because the practical limitations of working in the rainforest mean \
that data sampling is biased away from the center of the Amazon basin, and \
both explanations are reasonably well supported by the available data.

Q: What does LGM stands for?
A: Last Glacial Maximum.

Q: What did the analysis from the sediment deposits indicate?
A: Rainfall in the basin during the LGM was lower than for the present.

Q: What are some of scientists arguments?
A: The rainforest was reduced to small, isolated refugia separated by open forest and grassland.

Q: There have been major changes in Amazon rainforest vegetation over the last how many years?
A: 21,000.

Q: What caused changes in the Amazon rainforest vegetation?
A: The Last Glacial Maximum (LGM) and subsequent deglaciation

Q: What has been analyzed to compare Amazon rainfall in the past and present?
A: Sediment deposits.

Q: What has the lower rainfall in the Amazon during the LGM been attributed to?
A:''',
      temperature=temperature,
      max_output_tokens=256,
      top_k=1,
      top_p=0,
    )
    print(f"Response from Model: {response.text}")
# [END generativeai_sdk_extraction]

    return response


if __name__ == "__main__":
    extractive_question_answering()

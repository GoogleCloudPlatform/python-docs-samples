# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START vision_batch_annotate_files]

import io

from google.cloud import vision_v1


def sample_batch_annotate_files(file_path="path/to/your/document.pdf"):
    """Perform batch file annotation."""
    client = vision_v1.ImageAnnotatorClient()

    # Supported mime_type: application/pdf, image/tiff, image/gif
    mime_type = "application/pdf"
    with open(file_path, "rb") as f:
        content = f.read()
    input_config = {"mime_type": mime_type, "content": content}
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    # The service can process up to 5 pages per document file. Here we specify
    # the first, second, and last page of the document to be processed.
    pages = [1, 2, -1]
    requests = [{"input_config": input_config, "features": features, "pages": pages}]

    response = client.batch_annotate_files(requests=requests)
    for image_response in response.responses[0].responses:
        print(f"Full text: {image_response.full_text_annotation.text}")
        for page in image_response.full_text_annotation.pages:
            for block in page.blocks:
                print(f"\nBlock confidence: {block.confidence}")
                for par in block.paragraphs:
                    print(f"\tParagraph confidence: {par.confidence}")
                    for word in par.words:
                        print(f"\t\tWord confidence: {word.confidence}")
                        for symbol in word.symbols:
                            print(
                                "\t\t\tSymbol: {}, (confidence: {})".format(
                                    symbol.text, symbol.confidence
                                )
                            )


# [END vision_batch_annotate_files]

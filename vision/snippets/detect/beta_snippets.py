#!/usr/bin/env python

# Copyright 2018 Google LLC
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

"""
Google Cloud Vision API Python Beta Snippets

Example Usage:
python beta_snippets.py -h
python beta_snippets.py object-localization INPUT_IMAGE
python beta_snippets.py object-localization-uri gs://...
python beta_snippets.py handwritten-ocr INPUT_IMAGE
python beta_snippets.py handwritten-ocr-uri gs://...
python beta_snippets.py batch-annotate-files INPUT_PDF
python beta_snippets.py batch-annotate-files-uri gs://...
python beta_snippets.py batch-annotate-images-uri gs://... gs://...


For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io


# [START vision_localize_objects_beta]
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
# [END vision_localize_objects_beta]


# [START vision_localize_objects_gcs_beta]
def localize_objects_uri(uri):
    """Localize objects in the image on Google Cloud Storage

    Args:
    uri: The path to the file in Google Cloud Storage (gs://...)
    """
    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
# [END vision_localize_objects_gcs_beta]


# [START vision_handwritten_ocr_beta]
def detect_handwritten_ocr(path):
    """Detects handwritten characters in a local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image,
                                              image_context=image_context)

    print('Full Text: {}'.format(response.full_text_annotation.text))
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
# [END vision_handwritten_ocr_beta]


# [START vision_handwritten_ocr_gcs_beta]
def detect_handwritten_ocr_uri(uri):
    """Detects handwritten characters in the file located in Google Cloud
    Storage.

    Args:
    uri: The path to the file in Google Cloud Storage (gs://...)
    """
    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image,
                                              image_context=image_context)

    print('Full Text: {}'.format(response.full_text_annotation.text))
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
# [END vision_handwritten_ocr_gcs_beta]


# [START vision_batch_annotate_files_beta]
def detect_batch_annotate_files(path):
    """Detects document features in a PDF/TIFF/GIF file.

    While your PDF file may have several pages,
    this API can process up to 5 pages only.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision_v1p4beta1 as vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as pdf_file:
        content = pdf_file.read()

    # Other supported mime_types: image/tiff' or 'image/gif'
    mime_type = 'application/pdf'
    input_config = vision.InputConfig(
        content=content, mime_type=mime_type)

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    # Annotate the first two pages and the last one (max 5 pages)
    # First page starts at 1, and not 0. Last page is -1.
    pages = [1, 2, -1]

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=[feature],
        pages=pages)

    response = client.batch_annotate_files(requests=[request])

    for image_response in response.responses[0].responses:
        for page in image_response.full_text_annotation.pages:
            for block in page.blocks:
                print(u'\nBlock confidence: {}\n'.format(block.confidence))
                for par in block.paragraphs:
                    print(u'\tParagraph confidence: {}'.format(par.confidence))
                    for word in par.words:
                        symbol_texts = [symbol.text for symbol in word.symbols]
                        word_text = ''.join(symbol_texts)
                        print(u'\t\tWord text: {} (confidence: {})'.format(
                            word_text, word.confidence))
                        for symbol in word.symbols:
                            print(u'\t\t\tSymbol: {} (confidence: {})'.format(
                                symbol.text, symbol.confidence))
# [END vision_batch_annotate_files_beta]


# [START vision_batch_annotate_files_gcs_beta]
def detect_batch_annotate_files_uri(gcs_uri):
    """Detects document features in a PDF/TIFF/GIF file.

    While your PDF file may have several pages,
    this API can process up to 5 pages only.

    Args:
    uri: The path to the file in Google Cloud Storage (gs://...)
    """
    from google.cloud import vision_v1p4beta1 as vision
    client = vision.ImageAnnotatorClient()

    # Other supported mime_types: image/tiff' or 'image/gif'
    mime_type = 'application/pdf'
    input_config = vision.InputConfig(
        gcs_source=vision.GcsSource(uri=gcs_uri), mime_type=mime_type)

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    # Annotate the first two pages and the last one (max 5 pages)
    # First page starts at 1, and not 0. Last page is -1.
    pages = [1, 2, -1]

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=[feature],
        pages=pages)

    response = client.batch_annotate_files(requests=[request])

    for image_response in response.responses[0].responses:
        for page in image_response.full_text_annotation.pages:
            for block in page.blocks:
                print(u'\nBlock confidence: {}\n'.format(block.confidence))
                for par in block.paragraphs:
                    print(u'\tParagraph confidence: {}'.format(par.confidence))
                    for word in par.words:
                        symbol_texts = [symbol.text for symbol in word.symbols]
                        word_text = ''.join(symbol_texts)
                        print(u'\t\tWord text: {} (confidence: {})'.format(
                            word_text, word.confidence))
                        for symbol in word.symbols:
                            print(u'\t\t\tSymbol: {} (confidence: {})'.format(
                                symbol.text, symbol.confidence))
# [END vision_batch_annotate_files_gcs_beta]


# [START vision_async_batch_annotate_images_beta]
def async_batch_annotate_images_uri(input_image_uri, output_uri):
    """Batch annotation of images on Google Cloud Storage asynchronously.

    Args:
    input_image_uri: The path to the image in Google Cloud Storage (gs://...)
    output_uri: The path to the output path in Google Cloud Storage (gs://...)
    """
    import re

    from google.cloud import storage

    from google.cloud import vision_v1p4beta1 as vision
    client = vision.ImageAnnotatorClient()

    # Construct the request for the image(s) to be annotated:
    image_source = vision.ImageSource(image_uri=input_image_uri)
    image = vision.Image(source=image_source)
    features = [
        vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
        vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION),
        vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES),
    ]
    requests = [
        vision.AnnotateImageRequest(image=image, features=features),
    ]

    gcs_destination = vision.GcsDestination(uri=output_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=2)

    operation = client.async_batch_annotate_images(
        requests=requests, output_config=output_config)

    print('Waiting for the operation to finish.')
    operation.result(timeout=10000)

    # Once the request has completed and the output has been
    # written to Google Cloud Storage, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', output_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # Lists objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Processes the first output file from Google Cloud Storage.
    # Since we specified batch_size=2, the first response contains
    # annotations for the first two annotate image requests.
    output = blob_list[0]

    json_string = output.download_as_bytes().decode("utf-8")
    response = vision.BatchAnnotateImagesResponse.from_json(json_string)

    # Prints the actual response for the first annotate image request.
    print(u'The annotation response for the first request: {}'.format(
        response.responses[0]))
# [END vision_async_batch_annotate_images_beta]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    object_parser = subparsers.add_parser(
        'object-localization', help=localize_objects.__doc__)
    object_parser.add_argument('path')

    object_uri_parser = subparsers.add_parser(
        'object-localization-uri', help=localize_objects_uri.__doc__)
    object_uri_parser.add_argument('uri')

    handwritten_parser = subparsers.add_parser(
        'handwritten-ocr', help=detect_handwritten_ocr.__doc__)
    handwritten_parser.add_argument('path')

    handwritten_uri_parser = subparsers.add_parser(
        'handwritten-ocr-uri', help=detect_handwritten_ocr_uri.__doc__)
    handwritten_uri_parser.add_argument('uri')

    batch_annotate_parser = subparsers.add_parser(
        'batch-annotate-files', help=detect_batch_annotate_files.__doc__)
    batch_annotate_parser.add_argument('path')

    batch_annotate_uri_parser = subparsers.add_parser(
        'batch-annotate-files-uri',
        help=detect_batch_annotate_files_uri.__doc__)
    batch_annotate_uri_parser.add_argument('uri')

    batch_annotate__image_uri_parser = subparsers.add_parser(
        'batch-annotate-images-uri',
        help=async_batch_annotate_images_uri.__doc__)
    batch_annotate__image_uri_parser.add_argument('uri')
    batch_annotate__image_uri_parser.add_argument('output')

    args = parser.parse_args()

    if 'uri' in args.command:
        if 'object-localization-uri' in args.command:
            localize_objects_uri(args.uri)
        elif 'handwritten-ocr-uri' in args.command:
            detect_handwritten_ocr_uri(args.uri)
        elif 'batch-annotate-files-uri' in args.command:
            detect_batch_annotate_files_uri(args.uri)
        elif 'batch-annotate-images-uri' in args.command:
            async_batch_annotate_images_uri(args.uri, args.output)
    else:
        if 'object-localization' in args.command:
            localize_objects(args.path)
        elif 'handwritten-ocr' in args.command:
            detect_handwritten_ocr(args.path)
        elif 'batch-annotate-files' in args.command:
            detect_batch_annotate_files(args.path)

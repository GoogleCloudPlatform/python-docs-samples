# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_ocr_setup]
import base64
import json
import os
from typing import Any

from google.cloud import pubsub_v1
from google.cloud import storage
from google.cloud import translate_v2 as translate
from google.cloud import vision

vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()
storage_client = storage.Client()

project_id = os.environ["GCP_PROJECT"]
# [END functions_ocr_setup]


# [START functions_ocr_detect]
def detect_text(bucket: str, filename: str) -> None:
    """
    Extract the text from an image uploaded to Cloud Storage, then
    publish messages requesting subscribing services translate the text
    to each target language and save the result.

    Args:
        bucket: name of GCS bucket in which the file is stored.
        filename: name of the file to be read.

    Returns:
        None; the output is written to stdout and Stackdriver Logging.
    """
    print("Looking for text in image {}".format(filename))

    futures = []

    image = vision.Image(
        source=vision.ImageSource(gcs_image_uri=f"gs://{bucket}/{filename}")
    )
    text_detection_response = vision_client.text_detection(image=image)
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""
    print("Extracted text {} from image ({} chars).".format(text, len(text)))

    detect_language_response = translate_client.detect_language(text)
    src_lang = detect_language_response["language"]
    print("Detected language {} for text {}.".format(src_lang, text))

    # Submit a message to the bus for each target language
    to_langs = os.environ["TO_LANG"].split(",")
    for target_lang in to_langs:
        topic_name = os.environ["TRANSLATE_TOPIC"]
        if src_lang == target_lang or src_lang == "und":
            topic_name = os.environ["RESULT_TOPIC"]
        message = {
            "text": text,
            "filename": filename,
            "lang": target_lang,
            "src_lang": src_lang,
        }
        message_data = json.dumps(message).encode("utf-8")
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, data=message_data)
        futures.append(future)
    for future in futures:
        future.result()


# [END functions_ocr_detect]


# [START message_validatation_helper]
def validate_message(message: dict, param: str) -> Any:
    """
    Placeholder function for validating message parts.

    Args:
        message: message to be validated.
        param: name of the message parameter to be validated.

    Returns:
        The value of message['param'] if it's valid. Throws ValueError
        if it's not valid.
    """
    var = message.get(param)
    if not var:
        raise ValueError(
            "{} is not provided. Make sure you have \
                          property {} in the request".format(
                param, param
            )
        )
    return var
# [END message_validatation_helper]


# [START functions_ocr_process]
def process_image(file_info: dict, context: dict) -> None:
    """Cloud Function triggered by Cloud Storage when a file is changed.

    Args:
        file_info: Metadata of the changed file, provided by the
            triggering Cloud Storage event.
        context: a dictionary containing metadata about the event.

    Returns:
        None; the output is written to stdout and Stackdriver Logging.
    """
    bucket = validate_message(file_info, "bucket")
    name = validate_message(file_info, "name")

    detect_text(bucket, name)

    print("File {} processed.".format(file_info["name"]))


# [END functions_ocr_process]


# [START functions_ocr_translate]
def translate_text(event: dict, context: dict) -> None:
    """
    Cloud Function triggered by PubSub when a message is received from
    a subscription.

    Translates the text in the message from the specified source language
    to the requested target language, then sends a message requesting another
    service save the result.

    Args:
        event: dictionary containing the PubSub event.
        context: a dictionary containing metadata about the event.

    Returns:
        None; the output is written to stdout and Stackdriver Logging.
    """
    if event.get("data"):
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        message = json.loads(message_data)
    else:
        raise ValueError("Data sector is missing in the Pub/Sub message.")

    text = validate_message(message, "text")
    filename = validate_message(message, "filename")
    target_lang = validate_message(message, "lang")
    src_lang = validate_message(message, "src_lang")

    print("Translating text into {}.".format(target_lang))
    translated_text = translate_client.translate(
        text, target_language=target_lang, source_language=src_lang
    )
    topic_name = os.environ["RESULT_TOPIC"]
    message = {
        "text": translated_text["translatedText"],
        "filename": filename,
        "lang": target_lang,
    }
    encoded_message = json.dumps(message).encode("utf-8")
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, data=encoded_message)
    future.result()


# [END functions_ocr_translate]


# [START functions_ocr_save]
def save_result(event: dict, context: dict) -> None:
    """
    Cloud Function triggered by PubSub when a message is received from
    a subscription.

    Args:
        event: dictionary containing the PubSub event.
        context: a dictionary containing metadata about the event.

    Returns:
        None; the output is written to stdout and Stackdriver Logging.
    """
    if event.get("data"):
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        message = json.loads(message_data)
    else:
        raise ValueError("Data sector is missing in the Pub/Sub message.")

    text = validate_message(message, "text")
    filename = validate_message(message, "filename")
    lang = validate_message(message, "lang")

    print("Received request to save file {}.".format(filename))

    bucket_name = os.environ["RESULT_BUCKET"]
    result_filename = "{}_{}.txt".format(filename, lang)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(result_filename)

    print("Saving result to {} in bucket {}.".format(result_filename, bucket_name))

    blob.upload_from_string(text)

    print("File saved.")


# [END functions_ocr_save]

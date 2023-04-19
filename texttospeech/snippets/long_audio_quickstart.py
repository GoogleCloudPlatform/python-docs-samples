#!/usr/bin/env python
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All Rights Reserved.

from google.cloud import texttospeech
import time
import argparse

def synthesize_long_audio(text, language_code, voice_name, parent, output_gcs_uri):
  """
  Synthesizes long input, writing the resulting audio to `output_gcs_uri`.
  
  Example usage: synthesize_long_audio('Some input text to synthesize', 'en-US', 'en-US-Standard-A', 
  'projects/{PROJECT_NUMBER}/locations/{LOCATION}', 'gs://{BUCKET_NAME}/{OUTPUT_FILE_NAME}.wav')
  
  """
  # TODO(developer): Uncomment and set the following variables
  # text = "YOUR_INPUT_TEXT"
  # language_code = "YOUR_LANGUAGE_CODE"
  # voice_name = "YOUR_VOICE_NAME"
  # parent = "YOUR_PARENT_STRING"
  # output_gcs_uri = "YOUR_OUTPUT_GCS_URI"

  client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

  input = texttospeech.SynthesisInput()

  input.text = input_text

  audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

  voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)

  request = texttospeech.SynthesizeLongAudioRequest(parent=parent, input=input, audio_config=audio_config, voice=voice, output_gcs_uri=output_gcs_uri)

  operation = client.synthesize_long_audio(request=request)

  attempts = 0
  while (!operation.done and attempts < 30):
    print("Operation is still not done. Sleeping for 5 seconds and then trying again...")
    time.sleep(5)
    attempts += 1
  if attempts == 30:
    print("It's taking a while for your operation to complete. If the input was very large, this may be okay. If not, it likely means there was a failure.")
    return False
  print("Your operation is complete; check your GCS bucket to find your audio file!"
  return True

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

from google.cloud import texttospeech
import time

def synthesize_long_audio(project_id, location, output_gcs_uri):
  """
  Synthesizes long input, writing the resulting audio to `output_gcs_uri`.
  
  Example usage: synthesize_long_audio('12345', 'us-central1', 'gs://{BUCKET_NAME}/{OUTPUT_FILE_NAME}.wav')
  
  """
  # TODO(developer): Uncomment and set the following variables
  # parent = 'YOUR_PROJECT_ID'
  # location = 'YOUR_LOCATION'
  # output_gcs_uri = 'YOUR_OUTPUT_GCS_URI'

  client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

  input = texttospeech.SynthesisInput(text="Test input. Replace this with any text you want to synthesize, up to 1 million bytes long!")

  audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

  voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-A")
  
  parent = 'projects/' + project_id + '/locations/' + location

  request = texttospeech.SynthesizeLongAudioRequest(parent=parent, input=input, audio_config=audio_config, voice=voice, output_gcs_uri=output_gcs_uri)

  operation = client.synthesize_long_audio(request=request)
  
  result = operation.result(timeout=120)
  print("\nFinished processing, check your GCS bucket to find your audio file!")

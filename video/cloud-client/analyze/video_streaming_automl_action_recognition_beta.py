#
# Copyright 2020 Google LLC
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

# [START video_streaming_automl_action_recognition_beta]
import io
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from google.cloud.videointelligence_v1p3beta1 import enums


def streaming_automl_action_recognition(path, project_id, model_id):

    # path = 'path_to_file'
    # project_id = 'gcp_project_id'
    # model_id = 'automl_action_recognition_model_id'

    client = videointelligence.StreamingVideoIntelligenceServiceClient()

    model_path = "projects/{}/locations/us-central1/models/{}".format(
        project_id, model_id
    )

    automl_config = videointelligence.types.StreamingAutomlActionRecognitionConfig(
        model_name=model_path
    )

    video_config = videointelligence.types.StreamingVideoConfig(
        feature=enums.StreamingFeature.STREAMING_AUTOML_ACTION_RECOGNITION,
        automl_action_recognition_config=automl_config,
    )

    # config_request should be the first in the stream of requests.
    config_request = videointelligence.types.StreamingAnnotateVideoRequest(
        video_config=video_config
    )

    # Set the chunk size to 5MB (recommended less than 10MB).
    chunk_size = 5 * 1024 * 1024

    # Load file content.
    # Note: Input videos must have supported video codecs. See
    # https://cloud.google.com/video-intelligence/docs/streaming/streaming#supported_video_codecs
    # for more details.
    stream = []
    with io.open(path, "rb") as video_file:
        while True:
            data = video_file.read(chunk_size)
            if not data:
                break
            stream.append(data)

    def stream_generator():
        yield config_request
        for chunk in stream:
            yield videointelligence.types.StreamingAnnotateVideoRequest(
                input_content=chunk
            )

    requests = stream_generator()

    # streaming_annotate_video returns a generator.
    # The default timeout is about 300 seconds.
    # To process longer videos it should be set to
    # larger than the length (in seconds) of the stream.
    responses = client.streaming_annotate_video(requests, timeout=600)

    for response in responses:
        # Check for errors.
        if response.error.message:
            print(response.error.message)
            break

        for label in response.annotation_results.label_annotations:
            for frame in label.frames:
                print(
                    "At {:3d}s segment, {:5.1%} {}".format(
                        frame.time_offset.seconds,
                        frame.confidence,
                        label.entity.entity_id,
                    )
                )
# [END video_streaming_automl_action_recognition_beta]

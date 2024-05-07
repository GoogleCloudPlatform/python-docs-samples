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


def generate_content(PROJECT_ID: str, REGION: str, MODEL_ID: str) -> dict:
    # [START generativeaionvertexai_multimodal_embedding_advanced]
    # @title Client for multimodal embedding
    import time
    import typing
    from dataclasses import dataclass

    # Need to do pip install google-cloud-aiplatform for the following two imports.
    # Also run: gcloud auth application-default login.
    from google.cloud import aiplatform
    from google.protobuf import struct_pb2

    IMAGE_URI = "gs://cloud-samples-data/generative-ai/image/daisy.jpg"
    TEXT = "white shoes"
    VIDEO_URI = "gs://cloud-samples-data/generative-ai/video/animals.mp4"
    VIDEO_START_OFFSET_SEC = 10
    VIDEO_END_OFFSET_SEC = 60
    VIDEO_EMBEDDING_INTERVAL_SEC = 10
    DIMENSION = 128

    # Inspired from https://stackoverflow.com/questions/34269772/type-hints-in-namedtuple.
    class EmbeddingResponse(typing.NamedTuple):
        @dataclass
        class VideoEmbedding:
            start_offset_sec: int
            end_offset_sec: int
            embedding: typing.Sequence[float]

        text_embedding: typing.Sequence[float]
        image_embedding: typing.Sequence[float]
        video_embeddings: typing.Sequence[VideoEmbedding]

    class EmbeddingPredictionClient:
        """Wrapper around Prediction Service Client."""

        def __init__(self, project: str,
                     location: str = REGION,
                     api_regional_endpoint: str = f"{REGION}-aiplatform.googleapis.com") -> None:
            client_options = {"api_endpoint": api_regional_endpoint}
            # Initialize client that will be used to create and send requests.
            # This client only needs to be created once, and can be reused for multiple requests.
            self.client = aiplatform.gapic.PredictionServiceClient(
                client_options=client_options)
            self.location = location
            self.project = project

        def get_embedding(self, text: str = None, image_uri: str = None, video_uri: str = None,
                          start_offset_sec: int = 0, end_offset_sec: int = 120, interval_sec: int = 16, dimension = 1408) -> EmbeddingResponse:
            if not text and not image_uri and not video_uri:
                raise ValueError(
                    'At least one of text or image_uri or video_uri must be specified.')

            instance = struct_pb2.Struct()
            if text:
                instance.fields['text'].string_value = text

            if image_uri:
                image_struct = instance.fields['image'].struct_value
                image_struct.fields['gcsUri'].string_value = image_uri

            if video_uri:
                video_struct = instance.fields['video'].struct_value
                video_struct.fields['gcsUri'].string_value = video_uri
                video_config_struct = video_struct.fields['videoSegmentConfig'].struct_value
                video_config_struct.fields['startOffsetSec'].number_value = start_offset_sec
                video_config_struct.fields['endOffsetSec'].number_value = end_offset_sec
                video_config_struct.fields['intervalSec'].number_value = interval_sec

            parameters = struct_pb2.Struct()
            parameters.fields['dimension'].number_value = dimension

            instances = [instance]
            endpoint = (f"projects/{self.project}/locations/{self.location}"
                        f"/publishers/google/models/{MODEL_ID}")
            response = self.client.predict(
                endpoint=endpoint, instances=instances, parameters=parameters)

            text_embedding = None
            if text:
                text_emb_value = response.predictions[0]['textEmbedding']
                text_embedding = [v for v in text_emb_value]

            image_embedding = None
            if image_uri:
                image_emb_value = response.predictions[0]['imageEmbedding']
                image_embedding = [v for v in image_emb_value]

            video_embeddings = None
            if video_uri:
                video_emb_values = response.predictions[0]['videoEmbeddings']
                video_embeddings = [
                    EmbeddingResponse.VideoEmbedding(start_offset_sec=v['startOffsetSec'], end_offset_sec=v['endOffsetSec'],
                                                     embedding=[x for x in v['embedding']])
                    for v in
                    video_emb_values]

            return EmbeddingResponse(
                text_embedding=text_embedding,
                image_embedding=image_embedding,
                video_embeddings=video_embeddings)

    # client can be reused.
    client = EmbeddingPredictionClient(project=PROJECT_ID)
    start = time.time()
    response = client.get_embedding(text=TEXT, image_uri=IMAGE_URI, video_uri=VIDEO_URI,
                                    start_offset_sec=VIDEO_START_OFFSET_SEC,
                                    end_offset_sec=VIDEO_END_OFFSET_SEC,
                                    interval_sec=VIDEO_EMBEDDING_INTERVAL_SEC,
                                    dimension=DIMENSION)
    end = time.time()

    print(response)
    print('Time taken: ', end - start)
    # [END generativeaionvertexai_multimodal_embedding_advanced]

    return response

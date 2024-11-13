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

from vertexai.vision_models import MultiModalEmbeddingResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_image_video_text_embeddings() -> MultiModalEmbeddingResponse:
    """Example of how to generate multimodal embeddings from image, video, and text.

    Read more @ https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings#img-txt-vid-embedding
    """
    # [START generativeaionvertexai_multimodal_embedding_image_video_text]
    import vertexai

    from vertexai.vision_models import Image, MultiModalEmbeddingModel, Video
    from vertexai.vision_models import VideoSegmentConfig

    # TODO(developer): Update & uncomment line below
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

    image = Image.load_from_file(
        "gs://cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
    )
    video = Video.load_from_file(
        "gs://cloud-samples-data/vertex-ai-vision/highway_vehicles.mp4"
    )

    embeddings = model.get_embeddings(
        image=image,
        video=video,
        video_segment_config=VideoSegmentConfig(end_offset_sec=1),
        contextual_text="Cars on Highway",
    )

    print(f"Image Embedding: {embeddings.image_embedding}")

    # Video Embeddings are segmented based on the video_segment_config.
    print("Video Embeddings:")
    for video_embedding in embeddings.video_embeddings:
        print(
            f"Video Segment: {video_embedding.start_offset_sec} - {video_embedding.end_offset_sec}"
        )
        print(f"Embedding: {video_embedding.embedding}")

    print(f"Text Embedding: {embeddings.text_embedding}")
    # Example response:
    # Image Embedding: [-0.0123144267, 0.0727186054, 0.000201397663, ...]
    # Video Embeddings:
    # Video Segment: 0.0 - 1.0
    # Embedding: [-0.0206376351, 0.0345234685, ...]
    # Text Embedding: [-0.0207006838, -0.00251058186, ...]

    # [END generativeaionvertexai_multimodal_embedding_image_video_text]
    return embeddings


if __name__ == "__main__":
    get_image_video_text_embeddings()

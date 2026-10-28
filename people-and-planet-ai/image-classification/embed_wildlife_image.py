#!/usr/bin/env python

# Copyright 2026 Google LLC
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

# [START genai_wildlife_embed_image]
import sys

from google import genai
from google.genai import errors
from google.genai import types


def embed_wildlife_image(project_id: str, image_gcs_uri: str) -> None:
    """Generates a multimodal vector embedding for a camera trap image.

    Uses Gemini Embedding 2 on Gemini Enterprise Agent Platform using the
    global endpoint to project camera trap imagery into a 768-dimensional
    multimodal vector space suitable for few-shot rare species discovery and
    semantic search in BigQuery.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        image_gcs_uri: Cloud Storage URI of the camera trap JPEG image.
    """
    # gemini-embedding-2 serves on the global endpoint.
    location = "global"
    client = genai.Client(vertexai=True, project=project_id, location=location)

    image_part = types.Part.from_uri(
        file_uri=image_gcs_uri,
        mime_type="image/jpeg",
    )
    config = types.EmbedContentConfig(output_dimensionality=768)

    try:
        response = client.models.embed_content(
            model="gemini-embedding-2",
            contents=[image_part],
            config=config,
        )
    except errors.APIError as err:
        print(
            f"error: failed to embed camera trap image '{image_gcs_uri}' in "
            f"location '{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        values = response.embeddings[0].values
        preview = [round(v, 5) for v in values[:3]]
        print(f"Resource ID: {image_gcs_uri}")
        print(f"Embedding Dimensions: {len(values)}")
        print("Model: gemini-embedding-2")
        print(f"Sample Vector Values: {preview}")
# [END genai_wildlife_embed_image]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID.",
    )
    parser.add_argument(
        "--image-gcs-uri",
        default=(
            "gs://public-datasets-lila/wcs-unzipped/animals/0036/0072.jpg"
        ),
        help="Cloud Storage URI of the camera trap JPEG image.",
    )
    args = parser.parse_args()

    embed_wildlife_image(
        project_id=args.project,
        image_gcs_uri=args.image_gcs_uri,
    )

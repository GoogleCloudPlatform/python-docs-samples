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

# [START genai_wildlife_classify_image]
import sys

from google import genai
from google.genai import errors
from google.genai import types
from pydantic import BaseModel


class WildlifeObservation(BaseModel):
    species_scientific_name: str
    taxon_family: str
    common_name: str
    animal_count: int
    juvenile_present: bool
    is_empty_or_misfire: bool
    confidence: float


def classify_wildlife_image(
    project_id: str,
    image_gcs_uri: str,
    habitat_region: str = "Southeast Asia tropical rainforest",
) -> None:
    """Classifies a camera trap image into structured ecological metadata.

    Uses Gemini 3.8 Flash on Gemini Enterprise Agent Platform using the global
    endpoint with a Pydantic response schema and geographic habitat context
    (geo-fencing) to identify the species and taxonomic family, count
    individuals, detect juveniles, and flag empty or misfired frames.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        image_gcs_uri: Cloud Storage URI of the camera trap JPEG image.
        habitat_region: Geographic region used to ground species predictions.
    """
    # gemini-3.8-flash serves on the global endpoint.
    location = "global"
    client = genai.Client(vertexai=True, project=project_id, location=location)

    image_part = types.Part.from_uri(
        file_uri=image_gcs_uri,
        mime_type="image/jpeg",
    )
    habitat_prefix = (
        f"Camera trap habitat region: {habitat_region}. "
        if habitat_region
        else ""
    )
    prompt = (
        f"{habitat_prefix}"
        "Identify the wildlife species (scientific name, taxonomic family, and "
        "common name) in this camera trap photo, count the individuals, "
        "indicate whether juvenile offspring are present, and flag whether the "
        "frame is empty or a camera misfire."
    )
    thinking_config = types.ThinkingConfig(
        thinking_level=types.ThinkingLevel.LOW,
    )
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=WildlifeObservation,
        thinking_config=thinking_config,
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[image_part, prompt],
            config=config,
        )
    except errors.APIError as err:
        print(
            f"error: failed to classify camera trap image '{image_gcs_uri}' in "
            f"location '{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        observation = WildlifeObservation.model_validate_json(response.text)
        print(f"Resource ID: {image_gcs_uri}")
        print(f"Animal Count: {observation.animal_count}")
        print(f"Common Name: {observation.common_name}")
        print(f"Confidence: {observation.confidence:.2f}")
        print(f"Empty or Misfire: {observation.is_empty_or_misfire}")
        print(f"Habitat Region: {habitat_region}")
        print(f"Juvenile Present: {observation.juvenile_present}")
        print(f"Species: {observation.species_scientific_name}")
        print(f"Taxon Family: {observation.taxon_family}")
# [END genai_wildlife_classify_image]


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
    parser.add_argument(
        "--habitat-region",
        default="Southeast Asia tropical rainforest",
        help="Geographic region of the camera trap for geo-fenced classification.",
    )
    args = parser.parse_args()

    classify_wildlife_image(
        project_id=args.project,
        image_gcs_uri=args.image_gcs_uri,
        habitat_region=args.habitat_region,
    )

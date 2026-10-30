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

# [START googlegenaisdk_weather_analyze_storm_risk]
import os
import sys

from google import genai
from google.genai import errors
from google.genai import types

from pydantic import BaseModel


class StormRiskAssessment(BaseModel):
    storm_summary: str
    flood_risk_level: str
    orographic_amplification_risk: str
    peak_expected_rainfall_mm_hr: float
    recommended_actions: list[str]


def analyze_storm_risk(
    project_id: str,
    composite_image_path: str,
) -> None:
    """Generates a structured severe-weather and flood-risk report with Gemini.

    Combines a multi-band satellite and elevation composite image (GOES cloud
    moisture, NASA GPM IMERG V07 rainfall, and MERIT DEM topography) with
    BigQuery AI.FORECAST precipitation trajectories using Gemini 3.8 Flash on
    the global endpoint and a Pydantic response schema.

    Args:
        project_id: Google Cloud project identifier (for example, 'example-project-id').
        composite_image_path: Local path to the composite storm PNG image.
    """
    # gemini-3.8-flash serves on the global endpoint.
    location = "global"
    client = genai.Client(vertexai=True, project=project_id, location=location)

    with open(composite_image_path, "rb") as image_file:
        image_bytes = image_file.read()

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/png",
    )
    forecast_context = os.environ.get(
        "WEATHER_FORECAST_CONTEXT",
        "Storm: Hurricane Melissa (Jamaica Landfall, 18.1N 78.0W). "
        "Observed peak GPM IMERG V07 rainfall: 51.8 mm/hr over coastal and "
        "Blue Mountains terrain (elevation up to 2,256 m). "
        "BigQuery AI.FORECAST (TimesFM 2.5) next 6 hours trajectory: "
        "+1h: 38.4 mm/hr, +2h: 29.1 mm/hr, +3h: 21.7 mm/hr, "
        "+4h: 16.2 mm/hr, +5h: 12.0 mm/hr, +6h: 9.4 mm/hr.",
    )
    prompt = (
        f"{forecast_context} "
        "Examine the 3-panel satellite composite (left: GOES cloud & moisture, "
        "center: NASA GPM IMERG V07 precipitation rate in mm/hr, right: MERIT DEM "
        "terrain elevation in meters) alongside the TimesFM precipitation forecast. "
        "Provide a structured flood risk assessment, evaluate how steep mountain "
        "topography amplifies runoff and flash-flooding, and list concrete "
        "emergency response actions."
    )
    thinking_config = types.ThinkingConfig(
        thinking_level=types.ThinkingLevel.LOW,
    )
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=StormRiskAssessment,
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
            f"error: failed to analyze storm composite '{composite_image_path}' "
            f"in location '{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        assessment = StormRiskAssessment.model_validate_json(response.text)
        print(f"Resource ID: {composite_image_path}")
        print(f"Display Name: {assessment.flood_risk_level}")
        print(
            "Orographic Amplification Risk: "
            f"{assessment.orographic_amplification_risk}"
        )
        print(
            "Peak Expected Rainfall (mm/hr): "
            f"{assessment.peak_expected_rainfall_mm_hr:.1f}"
        )
        print(f"Storm Summary: {assessment.storm_summary}")
        for action in assessment.recommended_actions:
            print(f"  - {action}")


# [END googlegenaisdk_weather_analyze_storm_risk]


project_id_arg = os.environ.get("GOOGLE_CLOUD_PROJECT") or (
    sys.argv[1] if len(sys.argv) > 1 else None
)
if not project_id_arg:
    project_id_arg = "example-project-id"

image_path_arg = os.environ.get("STORM_COMPOSITE_IMAGE") or (
    sys.argv[2] if len(sys.argv) > 2 else None
)
if not image_path_arg:
    image_path_arg = "example-storm-composite.png"

if __name__ == "__main__":
    analyze_storm_risk(project_id_arg, image_path_arg)

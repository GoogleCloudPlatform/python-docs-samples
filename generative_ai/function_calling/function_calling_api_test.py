import os

import function_calling_basic
import function_calling_advanced


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"
MODEL_ID = "gemini-1.5-pro-preview-0409"


def test_function_calling_basic() -> None:
    response = function_calling_basic.generate_content(PROJECT_ID, REGION, MODEL_ID)
    assert response


def test_function_calling_advanced() -> None:
    response = function_calling_advanced.generate_content(PROJECT_ID, REGION, MODEL_ID)
    assert response
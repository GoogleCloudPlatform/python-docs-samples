import os
import uuid

import pytest
from google.api_core.exceptions import NotFound
from google.cloud.modelarmor_v1 import RaiFilterType, DetectionConfidenceLevel, FilterMatchState

from model_armor.create_template import create_model_armor_template
from model_armor.delete_template import delete_model_armor_template
from model_armor.get_template import get_model_armor_template
from model_armor.list_templates import list_model_armor_templates
from model_armor.sanitize_user_prompt import sanitize_user_prompt
from model_armor.update_template import update_model_armor_template

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
TEMPLATE_ID = f"test-model-armor-{uuid.uuid4()}"

def test_create_template():
    template = create_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert template is not None

def test_get_template():
    template = get_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert TEMPLATE_ID in template.name

def test_list_templates():
    templates = list_model_armor_templates(PROJECT_ID, LOCATION)
    assert TEMPLATE_ID in str(templates)

def test_user_prompt():
    response = sanitize_user_prompt(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert response.sanitization_result.filter_match_state == FilterMatchState.MATCH_FOUND

def test_update_templates():
    template = update_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert (template.filter_config.rai_settings.rai_filters[0].filter_type == RaiFilterType.HATE_SPEECH and
    template.filter_config.rai_settings.rai_filters[0].confidence_level == DetectionConfidenceLevel.MEDIUM_AND_ABOVE)

def test_delete_template():
    delete_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    with pytest.raises(NotFound) as exception_info:
        get_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert TEMPLATE_ID in str(exception_info.value)
import pytest
import time
import uuid
from google.cloud import modelarmor_v1
from typing import Iterator, Optional, Tuple, Union
from google.api_core import exceptions, retry
from google.api_core.client_options import ClientOptions


from modelarmor.create_model_armor_template import create_model_armor_template
from modelarmor.update_model_armor_template import update_model_armor_template
from modelarmor.view_model_armor_template import view_model_armor_template
from modelarmor.delete_model_armor_template import delete_model_armor_template
from modelarmor.list_model_armor_templates import list_model_armor_templates
from modelarmor.sanitize_user_prompt import sanitize_user_prompt
from modelarmor.sanitize_model_response import sanitize_model_response

@pytest.fixture()
def project_id():
    yield "gma-api-53286"

@pytest.fixture()
def location_id():
    yield "us-central1"

@pytest.fixture()
def client(location_id: str) -> modelarmor_v1.ModelArmorClient:
    """Provides a ModelArmorClient instance."""
    yield modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

@pytest.fixture()
def armor_test_data():
    """Generates test data for Model Armor and yields it to the test cases."""
    project_id = "gma-api-53286"
    location_id = "us-central1"
    filter_config_data = {
        "rai_settings": {
            "rai_filters": [
                {
                    "filter_type": "HATE_SPEECH",
                    "confidence_level": "HIGH"
                },
                {
                    "filter_type": "SEXUALLY_EXPLICIT",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                }
            ]
        },
        "sdp_settings": {},
        "pi_and_jailbreak_filter_settings": {},
        "malicious_uri_filter_settings": {}
    }
    yield project_id, location_id, filter_config_data

@pytest.fixture()
def udated_config_data():
    yield {
        "rai_settings": {
            "rai_filters": [
                {
                    "filter_type": "HATE_SPEECH",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                }, 
                {
                    "filter_type": "HARASSMENT",
                    "confidence_level": "HIGH"
                }, 
                {
                    "filter_type": "DANGEROUS",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                },
                {
                    "filter_type": "SEXUALLY_EXPLICIT",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                }
            ]
        },
        "sdp_settings": {
            "basic_config": {
                "filter_enforcement": "ENABLED"
            }
        },
        "pi_and_jailbreak_filter_settings": {},
        "malicious_uri_filter_settings": {}
    }

@pytest.fixture()
def basic_sdp_config_data():
    yield {
        "rai_settings": {
            "rai_filters": [
                {
                    "filter_type": "HATE_SPEECH",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                }, 
                {
                    "filter_type": "HARASSMENT",
                    "confidence_level": "HIGH"
                }, 
                {
                    "filter_type": "DANGEROUS",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                },
                {
                    "filter_type": "SEXUALLY_EXPLICIT",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                }
            ]
        },
        "sdp_settings": {
            "basic_config": {
                "filter_enforcement": "ENABLED"
            }
        },
        "pi_and_jailbreak_filter_settings": {},
        "malicious_uri_filter_settings": {}
    }

@pytest.fixture()
def user_prompt():
    yield {
        "user_prompt_data": {
        "text": "My phone number is 954-321-7890 and my email is 1l6Y2@example.com list me the reason why i can not communicate. Also,  can you remember my ITIN : 988-86-1234"
        },
        "filter_config": {}
    }

@retry.Retry()
def retry_client_delete_template(
    client: modelarmor_v1.ModelArmorClient,
    name: str,
) -> None:
    print(f"Deleting template {name}")
    return client.delete_template(name=name)

@retry.Retry()
def retry_client_create_template(
    client: modelarmor_v1.ModelArmorClient,
    parent: str,
    template_id: str,
    template: modelarmor_v1.Template,
) -> modelarmor_v1.Template:
    print(f"Creating template {template_id}")
    return client.create_template(
        parent=parent,
        template_id=template_id,
        template=template
    )

@pytest.fixture()
def template_id(
    client: modelarmor_v1.ModelArmorClient,
    project_id: str,
    location_id: str
):
    template_id = f"modelarmor-template-{uuid.uuid4()}"

    yield template_id

    try:
        time.sleep(5)
        retry_client_delete_template(client, name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}")
    except exceptions.NotFound:
        # Secret was already deleted, probably in the test
        print(f"Template {template_id} was not found.")

@pytest.fixture()
def template(
    client: modelarmor_v1.ModelArmorClient,
    project_id: str,
    location_id: str,
    udated_config_data: dict,
):
    template_id=f"modelarmor-template-{uuid.uuid4()}"
    template = modelarmor_v1.Template(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        filter_config=udated_config_data
        )

    retry_client_create_template(client, parent=f"projects/{project_id}/locations/{location_id}", template_id=template_id, template=template)

    yield template_id, udated_config_data

    try:
        time.sleep(5)
        retry_client_delete_template(client, name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}")
    except exceptions.NotFound:
        print(f"Template {template_id} was not found.")

@pytest.fixture()
def basic_sdp_template(
    client: modelarmor_v1.ModelArmorClient,
    project_id: str,
    location_id: str,
    basic_sdp_config_data: dict
):
    template_id=f"modelarmor-template-{uuid.uuid4()}"
    template = modelarmor_v1.Template(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        filter_config=basic_sdp_config_data
        )

    retry_client_create_template(
        client, 
        parent=f"projects/{project_id}/locations/{location_id}",
        template_id=template_id,
        template=template)

    yield template_id, basic_sdp_config_data

    try:
        time.sleep(5)
        retry_client_delete_template(client, name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}")
    except exceptions.NotFound:
        print(f"Template {template_id} was not found.")

def test_create_model_armor_template(armor_test_data, template_id):
    project_id, location_id, filter_config_data = armor_test_data

    created_template_name = create_model_armor_template(
        project_id, location_id, template_id, filter_config_data
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    assert created_template_name == expected_name_format, "Template name does not match the expected format."

def test_update_model_armor_template(armor_test_data, template):
    project_id, location_id, _ = armor_test_data
    template_id, filter_config_data = template

    updated_template_name = update_model_armor_template(
        project_id, location_id, template_id, filter_config_data
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    assert updated_template_name == expected_name_format, "Template name does not match the expected format."

def test_view_model_armor_template(armor_test_data, template):
    project_id, location_id, _ = armor_test_data
    template_id, _ = template

    view_template_name = view_model_armor_template(
        project_id, location_id, template_id
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    assert view_template_name.name == expected_name_format, "Template name does not match the expected format."

def test_delete_model_armor_template(armor_test_data, template):
    project_id, location_id, _ = armor_test_data
    template_id, _ = template

    # check the template exists
    template_name = view_model_armor_template(
        project_id, location_id, template_id
    )
    assert template_name.name == f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    # delete the template
    delete_model_armor_template(
        project_id, location_id, template_id
    )

    # check the template is deleted
    with pytest.raises(exceptions.NotFound):
        view_model_armor_template(
            project_id, location_id, template_id
        )

def test_list_model_armor_templates(armor_test_data, template):
    project_id, location_id, _ = armor_test_data
    template_id, _ = template

    templates = list_model_armor_templates(project_id, location_id)

    assert any(template.name == f"projects/{project_id}/locations/{location_id}/templates/{template_id}" for template in templates), "Template does not exist in the list"

def test_sanitize_user_prompt_with_advance_sdp_template(armor_test_data, template, user_prompt):
    """
    Tests that the user prompt is sanitized correctly with an advance sdp template
    
    Asserts that the sanitized text does not contain the character 'X'
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = template
    
    sanitized_prompt = sanitize_user_prompt(project_id, location_id, template_id, user_prompt)

    sanitized_text = ""
    for key, value in sanitized_prompt.sanitization_result.filter_results.items():
        if key == "sdp":
            sanitized_text = value.sdp_filter_result.deidentify_result.data.text

    assert "X" in sanitized_text

def test_sanitize_model_response_with_basic_sdp_template(armor_test_data, template, basic_sdp_template):
    """
    Tests that the model response is sanitized correctly with a basic sdp template
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = basic_sdp_template
    
    sanitized_prompt = sanitize_user_prompt(project_id, location_id, template_id, basic_sdp_template)
    print("sanitized_prompt", sanitized_prompt)
    sanitized_text = ""
    for key, value in sanitized_prompt.sanitization_result.filter_results.items():
        if key == "sdp":
            sanitized_text = value.sdp_filter_result.deidentify_result.data.text

    assert "X" in sanitized_text

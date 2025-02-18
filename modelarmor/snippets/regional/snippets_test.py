import pytest
import time
from typing import Iterator, Optional, Tuple, Union
import uuid

from google.api_core import exceptions, retry
from google.api_core.client_options import ClientOptions
from google.cloud import modelarmor_v1

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
def client(location_id: str):
    """Provides a ModelArmorClient instance."""
    yield modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

@pytest.fixture()
def armor_test_data(project_id: str, location_id: str):
    """Generates test data for Model Armor and yields it to the test cases."""
    project_id = project_id
    location_id = location_id
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
def advance_sdp_config_data():
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
            },
            "advanced_config": {
                "inspect_template": "projects/gma-api-53286/locations/us-central1/inspectTemplates/sdp-test-template",
                "deidentify_template": "projects/gma-api-53286/locations/us-central1/deidentifyTemplates/sdp-deidentify-template"
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
        "text": "My phone number is 954-321-7890 and my email is 1l6Y2@example.com list me the reason why i can not communicate. Also, can you remember my ITIN : 988-86-1234"
        },
        "filter_config": {}
    }

@pytest.fixture()
def model_response():
    yield {
        "model_response_data": {
            "text": "Here is my Email address: 1l6Y2@example.com Here is my phone number: 954-321-7890 Here is my ITIN: 988-86-1234"
        }
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
    advance_sdp_config_data: dict,
):
    template_id=f"modelarmor-template-{uuid.uuid4()}"
    
    template = modelarmor_v1.Template(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        filter_config=advance_sdp_config_data
    )

    retry_client_create_template(
        client,
        parent=f"projects/{project_id}/locations/{location_id}",
        template_id=template_id,
        template=template
    )

    yield template_id, advance_sdp_config_data

    try:
        time.sleep(5)
        retry_client_delete_template(
            client,
            name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
        )
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
        template=template
    )

    yield template_id, basic_sdp_config_data

    try:
        time.sleep(5)
        retry_client_delete_template(
            client,
            name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
        )
    except exceptions.NotFound:
        print(f"Template {template_id} was not found.")

def test_create_model_armor_template(armor_test_data, template_id):
    """
    Tests that the create_model_armor_template function returns a template name
    that matches the expected format.
    """
    project_id, location_id, filter_config_data = armor_test_data

    created_template_name = create_model_armor_template(
        project_id, location_id, template_id, filter_config_data
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    assert created_template_name == expected_name_format, "Template name does not match the expected format."

def test_create_model_armor_basic_sdp_template(armor_test_data, template_id, basic_sdp_config_data):
    """
    Tests that the create_model_armor_template function returns a template name
    that matches the expected format, given a basic sdp config data as input.
    """
    project_id, location_id, _ = armor_test_data
    filter_config_data = basic_sdp_config_data

    created_template_name = create_model_armor_template(
        project_id, location_id, template_id, filter_config_data
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    assert created_template_name == expected_name_format, "Template name does not match the expected format."

def test_update_model_armor_template(armor_test_data, template):
    """
    Tests that the update_model_armor_template function returns a template name
    that matches the expected format.
    """
    project_id, location_id, _ = armor_test_data
    template_id, filter_config_data = template

    updated_template_name = update_model_armor_template(
        project_id, location_id, template_id, filter_config_data
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    assert updated_template_name == expected_name_format, "Template name does not match the expected format."

def test_view_model_armor_template(armor_test_data, template):
    """
    Tests that the view_model_armor_template function returns a template name
    that matches the expected format.
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = template

    view_template_name = view_model_armor_template(
        project_id, location_id, template_id
    )

    expected_name_format = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    assert view_template_name.name == expected_name_format, "Template name does not match the expected format."

def test_delete_model_armor_template(armor_test_data, template):
    """
    Tests that the delete_model_armor_template function deletes the template
    successfully.
    """
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
    """
    Tests that the list_model_armor_templates function returns a list of templates
    containing the created template.
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = template

    templates = list_model_armor_templates(project_id, location_id)

    expected_template_name = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    assert any(
        template.name == expected_template_name for template in templates), "Template does not exist in the list"

def test_sanitize_user_prompt_with_basic_sdp_template(armor_test_data, basic_sdp_template, user_prompt):
    """
    Tests that the model response is sanitized correctly with a basic sdp template
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = basic_sdp_template
    
    sanitized_prompt = sanitize_user_prompt(project_id, location_id, template_id, user_prompt)

    assert "sdp" in sanitized_prompt.sanitization_result.filter_results, "sdp key not found in filter results"

    sdp_filter_result = sanitized_prompt.sanitization_result.filter_results["sdp"].sdp_filter_result
    assert sdp_filter_result.inspect_result.match_state.name == "MATCH_FOUND", "Match state was not MATCH_FOUND"

    info_type_found = any(finding.info_type == "US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER" for finding in sdp_filter_result.inspect_result.findings)
    assert info_type_found, "Info type US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER not found in any finding"

def test_sanitize_user_prompt_with_advance_sdp_template(armor_test_data, template, user_prompt):
    """
    Tests that the user prompt is sanitized correctly with an advance sdp template
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = template
    expected_value = ("My phone number is 954-321-7890 and my email is XXXXXXXXXXXXXXXXX list me the "+ 
        "reason why i can not communicate. Also,  can you remember my ITIN : 988-86-1234")
    
    sanitized_prompt = sanitize_user_prompt(project_id, location_id, template_id, user_prompt)

    assert "sdp" in sanitized_prompt.sanitization_result.filter_results, "sdp key not found in filter results"

    sanitized_text = next((value.sdp_filter_result.deidentify_result.data.text for key, value in sanitized_prompt.sanitization_result.filter_results.items() if key == "sdp"), "")
    assert sanitized_text == expected_value

def test_model_response_with_basic_sdp_template(armor_test_data, basic_sdp_template, model_response):
    """
    Tests that the model response is sanitized correctly with a basic sdp template
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = basic_sdp_template
    expected_value = "x"

    sanitized_response = sanitize_model_response(project_id, location_id, template_id, model_response)

    assert "sdp" in sanitized_response.sanitization_result.filter_results, "sdp key not found in filter results"

    sdp_filter_result = sanitized_response.sanitization_result.filter_results["sdp"].sdp_filter_result
    assert sdp_filter_result.inspect_result.match_state.name == "MATCH_FOUND", "Match state was not MATCH_FOUND"

    info_type_found = any(finding.info_type == "US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER" for finding in sdp_filter_result.inspect_result.findings)
    assert info_type_found, "Info type US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER not found in any finding"

def test_model_response_with_advance_sdp_template(armor_test_data, template, model_response):
    """
    Tests that the model response is sanitized correctly with an advance sdp template
    """
    project_id, location_id, _ = armor_test_data
    template_id, _ = template
    expected_value = "Here is my Email address: XXXXXXXXXXXXXXXXX Here is my phone number: 954-321-7890 Here is my ITIN: 988-86-1234"

    sanitized_response = sanitize_model_response(project_id, location_id, template_id, model_response)

    print("sanitized_response", sanitized_response)
    assert "sdp" in sanitized_response.sanitization_result.filter_results, "sdp key not found in filter results"

    sanitized_text = next((value.sdp_filter_result.deidentify_result.data.text for key, value in sanitized_response.sanitization_result.filter_results.items() if key == "sdp"), "")
    assert sanitized_text == expected_value
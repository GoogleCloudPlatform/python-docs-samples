from client.scc_client_beta import Asset

from creator.query.query_process_helper import (
    get_field_by_name,
    create_and_or_query_from_values
)


def test_create_and_or_query_from_values_multi_type():
    values = ['dandrade', 'joaog', 'honorio']
    field_name = 'securityCenterProperties.resourceOwners'
    field_type = 'MULTI'
    query_from_values = create_and_or_query_from_values(field_name, field_type, values)
    assert query_from_values == (' AND ( '
            'securityCenterProperties.resourceOwners : "dandrade" '
            'OR securityCenterProperties.resourceOwners : "joaog" '
            'OR securityCenterProperties.resourceOwners : "honorio" ) ')


def test_create_and_or_query_from_values_single_type():
    values = ['google.cloud.resourcemanager.Project',
              'google.compute.Firewall',
              'google.compute.Instance']
    field_name = 'securityCenterProperties.resourceType'
    field_type = 'SINGLE'
    query_from_values = create_and_or_query_from_values(field_name, field_type, values)
    assert query_from_values == (' AND ( '
            'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" '
            'OR securityCenterProperties.resourceType = "google.compute.Firewall" '
            'OR securityCenterProperties.resourceType = "google.compute.Instance" ) ')


def test_join_value_extract_attribute():
    mock_asset = {
        "securityCenterProperties": {
            "resourceType": "google.cloud.resourcemanager.Project"
        }
    }
    mock_asset = Asset(mock_asset, 'UNUSED')
    assert get_field_by_name(mock_asset, 'securityCenterProperties.resourceType') == 'google.cloud.resourcemanager.Project'


def test_join_value_extract_property():
    mock_asset = {
        "resourceProperties": {
            "name": 'asset-project'
        }
    }
    mock_asset = Asset(mock_asset, 'UNUSED')
    assert get_field_by_name(mock_asset, 'resourceProperties.name') == 'asset-project'


def test_join_value_extract_mark():
    mock_asset = {
        "securityMarks": {
            "marks": {
                "environment":"development"
            }
        }
    }
    mock_asset = Asset(mock_asset, 'UNUSED')
    assert get_field_by_name(mock_asset, 'securityMarks.marks.environment') == 'development'


def test_join_value_extract_mark_not_found():
    mock_asset = {
        "securityMarks": {
            "marks": {}
        }
    }
    mock_asset = Asset(mock_asset, 'UNUSED')
    assert get_field_by_name(mock_asset, 'securityMarks.marks.environment') is None


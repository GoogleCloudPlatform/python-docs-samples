import hashlib
import jsonpickle

from query_builder.domain_model.services.configuration_service import (
    get_organization_id,
    get_organization_display_name
)

def get_asset_result(owner, asset, marks, actual_query):
    asset.query = actual_query
    result_hash = __generate_result_hash(asset.name,
                                         asset.state,
                                         asset.updateTime)

    result_attributes = __get_asset_metadata_fields(owner,
                                                    asset,
                                                    marks,
                                                    result_hash)

    result = jsonpickle.encode(asset, unpicklable=False)
    return result, result_attributes


def get_finding_result(owner, finding, marks, actual_query):
    finding.query = actual_query
    result_hash = __generate_result_hash(finding.name,
                                         finding.state,
                                         finding.eventTime)

    result_attributes = __get_finding_metadata_fields(owner,
                                                      finding,
                                                      marks,
                                                      result_hash)

    result = jsonpickle.encode(finding, unpicklable=False)
    return result, result_attributes


def __generate_result_hash(*result_attributes):
    result_hash = ''
    for attr in result_attributes:
        result_hash += str(attr)
    return hashlib.md5(result_hash.encode()).hexdigest()


def __get_asset_metadata_fields(owner, asset, marks, asset_hash):
    org_display_name = get_organization_display_name()
    asset_type = asset.securityCenterProperties['resourceType']
    project_id = __get_project_asset_attr(asset, asset_type)
    fields = {'Notification-Type': "ASSETS",
              'Organization-Id': str(get_organization_id()),
              'Organization-Display-Name': str(org_display_name),
              'Project-Id': str(project_id),
              'Count': "1",
              'Event-Type': str(asset.state),
              'Asset-Type': str(asset_type),
              'Last-Updated-Time': str(asset.updateTime),
              'Asset-Id': str(asset.name),
              'Asset-Hash': str(asset_hash),
              'Marks':  str(marks),
              'Additional_Dest_Email': str(owner)}
    return fields


def __get_finding_metadata_fields(owner, source_finding, marks, finding_hash):
    org_display_name = get_organization_display_name()
    fields = {'Notification-Type': "FINDINGS",
              'Event-Type': str(source_finding.state),
              'Organization-Id': str(get_organization_id()),
              'Organization-Display-Name': str(org_display_name),
              'Project-Id': str(source_finding.name),
              'Count': "1",
              'Source-Id': str(source_finding.parent),
              'Asset-Id': str(source_finding.resourceName),
              'Category': str(source_finding.category),
              'Last-Updated-Time': str(source_finding.eventTime),
              'Finding-Id': str(source_finding.name),
              'Finding-Hash': str(finding_hash),
              'Marks':  str(marks),
              'Additional_Dest_Email': str(owner)}
    return fields


def __get_project_asset_attr(asset, asset_type):
    if asset_type == 'google.cloud.resourcemanager.Project':
        return asset.name
    if (asset_type == 'google.cloud.resourcemanager.Organization'
            or asset_type == 'google.cloud.resourcemanager.Folder'):
        return None
    return asset.securityCenterProperties['resourceParent']

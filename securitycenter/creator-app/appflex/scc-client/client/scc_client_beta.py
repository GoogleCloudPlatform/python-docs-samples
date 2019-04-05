# -*- coding: utf-8 -*-
import logging
import json
import os

from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# OS environment variables used by the client.
ENV_VAR_SCC_CLIENT_DEVELOPER_KEY = 'SCC_CLIENT_DEVELOPER_KEY'
ENV_VAR_SCC_CLIENT_APP_ENV = 'APP_ENV'
ENV_VAR_SCC_CLIENT_SERVICE_ACCOUNT_INFO = 'SCC_SERVICE_ACCOUNT'
ENV_VAR_SCC_CLIENT_SERVICE_ACCOUNT_FILE = 'SCC_SA_CLIENT_FILE'

# Auth scopes needed by the service.
CREDENTIAL_SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# URL for the discovery service.
SCC_CLIENT_DISCOVERY_SERVICE_URL_BASE = 'https://securitycenter.googleapis.com/$discovery/rest'

# File to look for the service account if the env variable has no value.
SCC_CLIENT_SERVICE_ACCOUNT_FILE_DEFAULT_NAME = 'accounts/cscc_api_client.json'

# Default value of size page on list requests
DEFAULT_PAGE_SIZE_LIST = 1000

LOGGER = logging.getLogger('scc_client')
LOGGER.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOGGER.addHandler(stream_handler)


# Datetime and duration helper functions.
def utcnow_in_google_datetime():
    return datetime.utcnow().isoformat() + 'Z'


class Asset(object):

    def __init__(self, d, state):
        self.__dict__ = d
        self.state = state


class Finding(object):

    def __init__(self, d):
        self.__dict__ = d


class Client(object):
    """SCC Beta API Client."""

    def __init__(self, organization_id,
                 default_page_size=DEFAULT_PAGE_SIZE_LIST,
                 default_max_pages=None):
        self.org_id = organization_id
        self.default_page_size = default_page_size
        self.default_max_pages = default_max_pages
        self.credentials = Client._load_credentials()
        self.developer_key = Client._get_developer_key()
        service_name = 'securitycenter'
        version = 'v1beta1'
        discovery_service_url = '{}?key={}'.format(
            SCC_CLIENT_DISCOVERY_SERVICE_URL_BASE,
            self.developer_key)
        self.service = Client._build_service(service_name,
                                             version,
                                             discovery_service_url,
                                             self.credentials)

    def list_assets(self, filter_expression=None, field_mask=None,
                    order_by=None, read_time=None, compare_duration=None):
        resource = self.service.organizations().assets()
        request = resource.list(parent='organizations/{}'.format(self.org_id),
                                filter=filter_expression,
                                fieldMask=field_mask,
                                orderBy=order_by,
                                readTime=read_time,
                                compareDuration=compare_duration,
                                pageSize=self.default_page_size)
        result_list = self._populate_result_list(request, resource,
                                                 'listAssetsResults', 'Asset')
        asset_list = []
        for result in result_list:
            asset = Asset(result['asset'], result['state'])
            asset_list.append(asset)
        return asset_list

    def list_findings(self, source='-', filter_expression=None,
                      field_mask=None, order_by=None, read_time=None):
        resource = self.service.organizations().sources().findings()
        parent = 'organizations/{}/sources/{}'.format(self.org_id, source)
        request = resource.list(parent=parent,
                                filter=filter_expression,
                                fieldMask=field_mask,
                                orderBy=order_by,
                                readTime=read_time,
                                pageSize=self.default_page_size)
        result_list = self._populate_result_list(request, resource, 'findings',
                                                 'Finding')
        findings_list = []
        for result in result_list:
            finding = Finding(result)
            findings_list.append(finding)
        return findings_list

    def update_asset_security_mark(self, security_marks_map,
                                   asset_id=None, asset_name=None):
        """Update the mark set on asset.
           If asset_name is set it will be used on resource name, if not, will be asset_id instead."""
        resource = self.service.organizations().assets()
        name = 'organizations/{}/assets/{}/securityMarks'.format(
            self.org_id, asset_id) if not asset_name else asset_name + '/securityMarks'
        return self._update_security_mark(resource, name, security_marks_map)

    def remove_asset_security_mark(self, mark, asset_id=None, asset_name=None):
        """Remove the mark set on asset.
           If asset_name is set it will be used on resource name, if not, will be asset_id instead."""
        resource = self.service.organizations().assets()
        name = 'organizations/{}/assets/{}/securityMarks'.format(
            self.org_id, asset_id) if not asset_name else asset_name + '/securityMarks'
        return self._remove_security_mark(resource, name, mark)

    def update_finding_security_mark(self, security_marks_map,
                                     source_id=None, finding_id=None,
                                     finding_name=None):
        """Update the mark set on finding.
           If finding_name is set it will be used on resource name, if not, will be source_id and finding_id instead."""
        resource = self.service.organizations().sources().findings()
        name = 'organizations/{}/sources/{}/findings/{}/securityMarks'.format(
            self.org_id, source_id, finding_id) if not finding_name else finding_name + '/securityMarks'
        return self._update_security_mark(resource, name, security_marks_map)

    def remove_finding_security_mark(self, security_mark,
                                     source_id=None, finding_id=None,
                                     finding_name=None):
        """Remove the mark set on finding.
           If finding_name is set it will be used on resource name, if not, will be source_id and finding_id instead."""
        resource = self.service.organizations().sources().findings()
        name = 'organizations/{}/sources/{}/findings/{}/securityMarks'.format(
            self.org_id, source_id, finding_id) if not finding_name else finding_name + '/securityMarks'
        return self._remove_security_mark(resource, name, security_mark)

    def create_finding(self, source_id, finding_id, category, state='ACTIVE',
                       resource_name=None, external_uri=None,
                       source_properties={}, security_marks={},
                       event_time=None):
        resource = self.service.organizations().sources().findings()
        parent = 'organizations/{}/sources/{}'.format(self.org_id, source_id)

        if event_time is None:
            event_time_str = utcnow_in_google_datetime()

        finding = {
            "category": category,
            "state": state,
            "resourceName": resource_name,
            "externalUri": external_uri,
            "sourceProperties": source_properties,
            "securityMarks": security_marks,
            "eventTime": event_time_str,
        }
        request = resource.create(parent=parent, findingId=finding_id,
                                  body=finding)
        return request.execute()

    @staticmethod
    def _remove_security_mark(resource, name, security_marks_map):
        update_mask = Client._mark_to_update_mask(security_marks_map)
        request = resource.updateSecurityMarks(name=name,
                                               updateMask=update_mask,
                                               body={"marks": None})
        return request.execute()

    @staticmethod
    def _update_security_mark(resource, name, security_marks_map):
        marks = {
            "marks": security_marks_map
        }
        update_mask = Client._mark_to_update_mask(security_marks_map)
        request = resource.updateSecurityMarks(name=name,
                                               body=marks,
                                               updateMask=update_mask)
        return request.execute()

    @staticmethod
    def _mark_to_update_mask(marks):
        return ','.join(
            ['marks.{}'.format(k.lower()) for k in marks.keys()]
        )

    def _populate_result_list(self, request, resource, results_list_attribute,
                              object_name):
        result_list = []
        pages = 0
        while request is not None \
                and (self.default_max_pages is None or
                     pages < self.default_max_pages):
            pages += 1
            response = request.execute()
            total_size = response.get('totalSize', 0)
            LOGGER.debug('%s: Total size=%s. Max pages=%s. Retrieving page %s.',
                         object_name,
                         total_size,
                         self.default_max_pages,
                         pages)

            result = response.get(results_list_attribute)

            if result is not None:
                result_list.extend(result)

            request = resource.list_next(request, response)
        return result_list

    @staticmethod
    def _load_credentials():
        if Client._is_production_runtime():
            credentials = Client._load_credentials_from_sa_info()
        else:
            credentials = Client._load_credentials_from_sa_file()

        return credentials.with_scopes(CREDENTIAL_SCOPES)

    @staticmethod
    def _get_developer_key():
        developer_key = os.getenv(ENV_VAR_SCC_CLIENT_DEVELOPER_KEY, None)
        if developer_key is None:
            raise RuntimeError(
                'The developer key should be provided in the env variable {}.'
                .format(ENV_VAR_SCC_CLIENT_DEVELOPER_KEY))
        else:
            return developer_key

    @staticmethod
    def _is_production_runtime():
        return os.getenv(ENV_VAR_SCC_CLIENT_APP_ENV, '') != ''

    @staticmethod
    def _load_credentials_from_sa_info():
        encoded_service_account = os.getenv(
            ENV_VAR_SCC_CLIENT_SERVICE_ACCOUNT_INFO, None)
        if encoded_service_account is None:
            raise RuntimeError(
                'Could not load credentials because the env variable {} has'
                'no value.'.format(ENV_VAR_SCC_CLIENT_SERVICE_ACCOUNT_INFO))
        else:
            service_account_info = json.loads(encoded_service_account)
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            return credentials

    @staticmethod
    def _load_credentials_from_sa_file():
        service_account_file = os.getenv(
            ENV_VAR_SCC_CLIENT_SERVICE_ACCOUNT_FILE, None)
        if service_account_file is None:
            LOGGER.warning('Env variable %s not set. Trying with the default value: %s.',
                           ENV_VAR_SCC_CLIENT_SERVICE_ACCOUNT_FILE,
                           SCC_CLIENT_SERVICE_ACCOUNT_FILE_DEFAULT_NAME)
            credentials = service_account.Credentials.from_service_account_file(
                SCC_CLIENT_SERVICE_ACCOUNT_FILE_DEFAULT_NAME)
        else:
            credentials = service_account.Credentials.from_service_account_file(service_account_file)
        return credentials

    @staticmethod
    def _build_service(service_name, version, discovery_service_url,
                       credentials):
        return build(service_name,
                     version,
                     discoveryServiceUrl=discovery_service_url,
                     credentials=credentials)


# def main():
#     client = Client('1055058813388', default_max_pages=3)
    # assets = client.list_assets(filter_expression='securityCenterProperties.resourceType : "Organization"',
    #                             read_time=utcnow_in_google_datetime(), compare_duration='120000000s')
    # LOGGER.info(json.dumps(assets, sort_keys=True, indent=2))
    # findings = client.list_findings(filter_expression='securityMarks.marks.scc_beta_client_test : "test"',
    #                                 read_time=utcnow_in_google_datetime())
    # LOGGER.info(json.dumps(findings, sort_keys=True, indent=2))
    # asset_marks = client.update_asset_security_mark({'scc_beta_client_test': 'test'},
    #                                                 asset_id='11712741160732498783')
    # LOGGER.info(json.dumps(asset_marks, sort_keys=True, indent=2))
    # findings_marks = client.update_finding_security_mark({'scc_beta_client_test': 'test'},
    #                                                      source_id='9264282320683959279',
    #                                                      found_id='a0a0a0a0a0a1')
    # LOGGER.info(json.dumps(findings_marks, sort_keys=True, indent=2))
    # new_finding = client.create_finding('9264282320683959279', 'a0a0a0a0a0b8', 'audit_log_test_category')
    # LOGGER.info(json.dumps(new_finding, sort_keys=True, indent=2))
    #
    # client.remove_asset_security_mark( 'sccbetaclienttest', asset_id='11712741160732498783')

# main()

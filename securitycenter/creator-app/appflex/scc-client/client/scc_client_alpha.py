import base64
import json
import os
import logging as logging
from time import sleep

from google.protobuf import duration_pb2, timestamp_pb2
from google.cloud import securitycenter
from google.oauth2 import service_account as sa
from .helpers import (
    duration_to_seconds,
    fixed_timestamp_to_seconds,
    from_now_to_seconds
)


LOGGER = logging.getLogger('scc_client')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOGGER.addHandler(stream_handler)

# Queries per Second allowed in the API calls
WAIT_TIME = 1 / float(os.getenv('QPS', '1000'))


class Client(object):
    """SCC client to use on scc tools projects"""

    ASSET_KIND = 'ASSET'
    FINDING_KIND = 'FINDING'

    def __init__(self):
        self.client = Client.__get_authenticated_cscc_client()

    @staticmethod
    def create_scc_params(where=None,
                          duration=None,
                          reference_time=None,
                          reference_time_type=None,
                          timeout=None):
        """Create params need to make a query on SCC"""
        query_args = {}
        if where:
            query_args['query'] = where
        if duration:
            query_args['compare_duration'] = duration_pb2.Duration(seconds=duration_to_seconds(duration))
        if reference_time:
            if reference_time_type == 'TIMESTAMP':
                query_args['reference_time'] = timestamp_pb2.Timestamp(
                    seconds=fixed_timestamp_to_seconds(reference_time))
            if reference_time_type == 'FROM_NOW':
                query_args['reference_time'] = timestamp_pb2.Timestamp(
                    seconds=from_now_to_seconds(reference_time))
        if timeout:
            query_args['timeout'] = int(timeout)
        return query_args

    def add_or_update_marks(self, marks, ids_by_kind):
        """Add or update marks on ids passed by kind"""
        for kind, new_ids in ids_by_kind.items():
            old_ids = self.__get_previous_execution_ids(kind, marks)
            to_remove = Client.__diff_marked_items_ids(old_ids, new_ids)
            to_add = Client.__diff_marked_items_ids(new_ids, old_ids)

            for remove_item in to_remove:
                self.remove_mark(kind, remove_item, marks)
                # awaits some time to achieve the QPS requirementes in case of removing findings marks
                if kind == self.FINDING_KIND:
                    sleep(WAIT_TIME)

            for add_item in to_add:
                self.add_mark(kind, add_item, marks)
                # awaits some time to achieve the QPS requirementes in case of adding findings marks
                if kind == self.FINDING_KIND:
                    sleep(WAIT_TIME)

    def execute_cscc_search(self, kind, query_args):
        """Runs a search on SCC with query args passed from specific kind"""
        organizations = Client.__get_current_organization()
        LOGGER.info("execute_cscc_search - Kind: %s - query_args: %s - organization: %s",kind, query_args, organizations)
        if kind == self.ASSET_KIND:
            return list(self.client.search_assets(
                organizations,
                **query_args))
        if kind == self.FINDING_KIND:
            return list(self.client.search_findings(
                organizations,
                **query_args))

    def add_mark(self, kind, _id, marks):
        """Add marks on specific scc kind"""
        LOGGER.info("add_mark - Kind: %s, id: %s, marks: %s",kind, _id, marks)
        if kind == self.ASSET_KIND:
            LOGGER.debug('__get_current_organization: %s, id: %s, add_or_update_marks: %s',
                      Client.__get_current_organization(),
                      _id,
                      Client.__lower_dict(marks))
            LOGGER.debug("add_mark - modify_asset: %s",
                self.client.modify_asset(
                Client.__get_current_organization(),
                _id,
                add_or_update_marks=Client.__lower_dict(marks)))
        if kind == self.FINDING_KIND:
            LOGGER.debug("add_mark - modify_finding: %s",
                self.client.modify_finding(
                Client.__get_current_organization(),
                _id,
                add_or_update_marks=Client.__lower_dict(marks)))

    def remove_mark(self, kind, _id, marks):
        """Remove marks on specific scc kind"""
        if kind == self.ASSET_KIND:
            LOGGER.debug("remove_mark - client.modify_asset: %s",
                self.client.modify_asset(
                    Client.__get_current_organization(),
                    _id,
                    remove_marks_with_keys=Client.__lower_dict(marks)))
        if kind == self.FINDING_KIND:
            LOGGER.debug("remove_mark - client.modify_finding: %s",
                self.client.modify_finding(
                Client.__get_current_organization(),
                _id,
                remove_marks_with_keys=Client.__lower_dict(marks)))

    @staticmethod
    def __diff_marked_items_ids(minuend_ids, subtrahend_ids):
        if minuend_ids:
            return minuend_ids.difference(subtrahend_ids)
        return set()

    @staticmethod
    def __lower_dict(_dict):
        return {key.lower(): value.lower() for key, value in _dict.items()}

    def __get_previous_execution_ids(self, kind, marks):
        resp = self.execute_cscc_search(
            kind, Client.__create_query_from_marks(marks))
        return set([x.id for x in resp])

    @staticmethod
    def __create_query_from_marks(marks):
        query_args = {'query': ' AND '.join(
            ['mark.' + key.lower() + ':' + '"' + value.lower().replace('working_', '') + '"'
             for key, value
             in marks.items()])
        }
        return query_args

    @staticmethod
    def __get_current_organization():
        return "organizations/" + str(os.getenv('organization_id'))

    @staticmethod
    def __get_authenticated_cscc_client():
        credentials = get_credentials()

        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])

        client = securitycenter.SecurityCenterClient(
            credentials=scoped_credentials)
        return client


def get_credentials():
    if os.getenv('APP_ENV', '') != '':
        service_account_info = get_service_account_json()
        return sa.Credentials.from_service_account_info(service_account_info)
    return sa.Credentials.from_service_account_file(os.getenv(
        'SCC_SA_CLIENT_FILE',
        'accounts/cscc_api_client.json'))


def get_service_account_json():
    enconded_service_account = os.getenv('SCC_SERVICE_ACCOUNT', None)
    if enconded_service_account is not None:
        return json.loads(enconded_service_account)
    return None
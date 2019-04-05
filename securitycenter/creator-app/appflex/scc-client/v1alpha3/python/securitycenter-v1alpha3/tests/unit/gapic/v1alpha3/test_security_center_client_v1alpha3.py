# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests."""

import pytest

from google.cloud import securitycenter_v1alpha3
from google.cloud.securitycenter_v1alpha3.proto import messages_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestSecurityCenterClient(object):
    def test_search_assets(self):
        # Setup Expected Response
        next_page_token = ''
        total_size = 705419236
        assets_element = {}
        assets = [assets_element]
        expected_response = {
            'next_page_token': next_page_token,
            'total_size': total_size,
            'assets': assets
        }
        expected_response = messages_pb2.SearchAssetsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup Request
        org_name = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.search_assets(org_name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.assets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = messages_pb2.SearchAssetsRequest(org_name=org_name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_assets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup request
        org_name = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.search_assets(org_name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_modify_asset(self):
        # Setup Expected Response
        id_2 = 'id23227150'
        parent_id = 'parentId2070327504'
        type_ = 'type3575610'
        expected_response = {'id': id_2, 'parent_id': parent_id, 'type': type_}
        expected_response = messages_pb2.Asset(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup Request
        org_name = client.organization_path('[ORGANIZATION]')
        id_ = 'id3355'

        response = client.modify_asset(org_name, id_)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = messages_pb2.ModifyAssetRequest(
            org_name=org_name, id=id_)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_modify_asset_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup request
        org_name = client.organization_path('[ORGANIZATION]')
        id_ = 'id3355'

        with pytest.raises(CustomException):
            client.modify_asset(org_name, id_)

    def test_search_findings(self):
        # Setup Expected Response
        next_page_token = ''
        total_size = 705419236
        findings_element = {}
        findings = [findings_element]
        expected_response = {
            'next_page_token': next_page_token,
            'total_size': total_size,
            'findings': findings
        }
        expected_response = messages_pb2.SearchFindingsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup Request
        org_name = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.search_findings(org_name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.findings[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = messages_pb2.SearchFindingsRequest(
            org_name=org_name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_findings_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup request
        org_name = client.organization_path('[ORGANIZATION]')

        paged_list_response = client.search_findings(org_name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_finding(self):
        # Setup Expected Response
        id_ = 'id3355'
        asset_id = 'assetId-373202742'
        scanner_id = 'scannerId-332541188'
        expected_response = {
            'id': id_,
            'asset_id': asset_id,
            'scanner_id': scanner_id
        }
        expected_response = messages_pb2.Finding(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup Request
        org_name = client.organization_path('[ORGANIZATION]')
        source_finding = {}

        response = client.create_finding(org_name, source_finding)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = messages_pb2.CreateFindingRequest(
            org_name=org_name, source_finding=source_finding)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_finding_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup request
        org_name = client.organization_path('[ORGANIZATION]')
        source_finding = {}

        with pytest.raises(CustomException):
            client.create_finding(org_name, source_finding)

    def test_modify_finding(self):
        # Setup Expected Response
        id_2 = 'id23227150'
        asset_id = 'assetId-373202742'
        scanner_id = 'scannerId-332541188'
        expected_response = {
            'id': id_2,
            'asset_id': asset_id,
            'scanner_id': scanner_id
        }
        expected_response = messages_pb2.Finding(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup Request
        org_name = client.organization_path('[ORGANIZATION]')
        id_ = 'id3355'

        response = client.modify_finding(org_name, id_)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = messages_pb2.ModifyFindingRequest(
            org_name=org_name, id=id_)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_modify_finding_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = securitycenter_v1alpha3.SecurityCenterClient(channel=channel)

        # Setup request
        org_name = client.organization_path('[ORGANIZATION]')
        id_ = 'id3355'

        with pytest.raises(CustomException):
            client.modify_finding(org_name, id_)

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
"""Accesses the google.cloud.securitycenter.v1alpha3 SecurityCenter API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from google.cloud.securitycenter_v1alpha3.gapic import enums
from google.cloud.securitycenter_v1alpha3.gapic import security_center_client_config
from google.cloud.securitycenter_v1alpha3.proto import messages_pb2
from google.cloud.securitycenter_v1alpha3.proto import services_pb2
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-securitycenter', ).version


class SecurityCenterClient(object):
    """Service for Cloud Security Command Center."""

    SERVICE_ADDRESS = 'securitycenter.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.securitycenter.v1alpha3.SecurityCenter'

    @classmethod
    def organization_path(cls, organization):
        """Return a fully-qualified organization string."""
        return google.api_core.path_template.expand(
            'organizations/{organization}',
            organization=organization,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=security_center_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.security_center_stub = (services_pb2.SecurityCenterStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._search_assets = google.api_core.gapic_v1.method.wrap_method(
            self.security_center_stub.SearchAssets,
            default_retry=method_configs['SearchAssets'].retry,
            default_timeout=method_configs['SearchAssets'].timeout,
            client_info=client_info,
        )
        self._modify_asset = google.api_core.gapic_v1.method.wrap_method(
            self.security_center_stub.ModifyAsset,
            default_retry=method_configs['ModifyAsset'].retry,
            default_timeout=method_configs['ModifyAsset'].timeout,
            client_info=client_info,
        )
        self._search_findings = google.api_core.gapic_v1.method.wrap_method(
            self.security_center_stub.SearchFindings,
            default_retry=method_configs['SearchFindings'].retry,
            default_timeout=method_configs['SearchFindings'].timeout,
            client_info=client_info,
        )
        self._create_finding = google.api_core.gapic_v1.method.wrap_method(
            self.security_center_stub.CreateFinding,
            default_retry=method_configs['CreateFinding'].retry,
            default_timeout=method_configs['CreateFinding'].timeout,
            client_info=client_info,
        )
        self._modify_finding = google.api_core.gapic_v1.method.wrap_method(
            self.security_center_stub.ModifyFinding,
            default_retry=method_configs['ModifyFinding'].retry,
            default_timeout=method_configs['ModifyFinding'].timeout,
            client_info=client_info,
        )

    # Service calls
    def search_assets(self,
                      org_name,
                      query=None,
                      order_by=None,
                      reference_time=None,
                      compare_duration=None,
                      page_size=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Search assets within an organization.

        Example:
            >>> from google.cloud import securitycenter_v1alpha3
            >>>
            >>> client = securitycenter_v1alpha3.SecurityCenterClient()
            >>>
            >>> org_name = client.organization_path('[ORGANIZATION]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_assets(org_name):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.search_assets(org_name, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            org_name (str): Name of the organization to search for assets. Its format is
                \"organizations/[organization_id]\". For example, \"organizations/1234\".
            query (str): Expression that defines the query to apply across assets.
                The expression is a list of one or more restrictions combined via logical
                operators ``AND`` and ``OR``.
                Parentheses are not supported, and ``OR`` has higher precedence than ``AND``.

                Restrictions have the form ``<field> <operator> <value>`` and may have a ``-``
                character in front of them to indicate negation. The fields can be of the
                following types:

                * Attribute: optional ``attribute.`` prefix or no prefix and name.
                * Property: mandatory ``property.`` prefix and name.
                * Mark: mandatory ``mark`` prefix and name.

                The supported operators are:

                * ``=`` for all value types.
                * ``>``, ``<``, ``>=``, ``<=`` for integer values.
                * ``:``, meaning substring matching, for strings.

                The supported value types are:

                * string literals in quotes.
                * integer literals without quotes.
                * boolean literals ``true`` and ``false`` without quotes.

                For example, ``property.count = 100`` is a valid query string.
            order_by (str): Expression that defines what fields and order to use for sorting.
            reference_time (Union[dict, ~google.cloud.securitycenter_v1alpha3.types.Timestamp]): Time at which to search for assets. The search will capture the state of
                assets at this point in time.

                Not providing a value or providing one in the future is treated as current.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.securitycenter_v1alpha3.types.Timestamp`
            compare_duration (Union[dict, ~google.cloud.securitycenter_v1alpha3.types.Duration]): When compare_duration is set, the Asset's \"state\" attribute is updated to
                indicate whether the asset was added, removed, or remained present during
                the compare_duration period of time that precedes the reference_time. This
                is the time between (reference_time - compare_duration) and reference_time.

                The state value is derived based on the presence of the asset at the two
                points in time. Intermediate state changes between the two times don't
                affect the result. For example, the results aren't affected if the asset is
                removed and re-created again.

                Possible \"state\" values when compare_duration is specified:

                * \"ADDED\": indicates that the asset was not present before
                ::

                             compare_duration, but present at reference_time.
                * \"REMOVED\": indicates that the asset was present at the start of
                ::

                             compare_duration, but not present at reference_time.
                * \"ACTIVE_AT_BOTH\": indicates that the asset was present at both the
                ::

                             start and the end of the time period defined by
                             compare_duration and reference_time.

                If compare_duration is not specified, then the only possible state is
                \"ACTIVE\", which indicates that the asset is present at reference_time.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.securitycenter_v1alpha3.types.Duration`
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.securitycenter_v1alpha3.types.Asset` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = messages_pb2.SearchAssetsRequest(
            org_name=org_name,
            query=query,
            order_by=order_by,
            reference_time=reference_time,
            compare_duration=compare_duration,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._search_assets,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='assets',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def modify_asset(self,
                     org_name,
                     id_,
                     add_or_update_marks=None,
                     remove_marks_with_keys=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Modifies the marks on the specified asset.

        Example:
            >>> from google.cloud import securitycenter_v1alpha3
            >>>
            >>> client = securitycenter_v1alpha3.SecurityCenterClient()
            >>>
            >>> org_name = client.organization_path('[ORGANIZATION]')
            >>>
            >>> # TODO: Initialize ``id_``:
            >>> id_ = ''
            >>>
            >>> response = client.modify_asset(org_name, id_)

        Args:
            org_name (str): Organization name.
            id_ (str): Unique identifier for the asset to be modified.
            add_or_update_marks (dict[str -> str]): Keys and values to add/update on the asset.

                If a mark with the same key already exists, its value will be replaced by
                the updated value.
            remove_marks_with_keys (list[str]): A list of keys defining the marks to remove from the asset. There can be no
                overlaps between keys to remove and keys to add or update.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.securitycenter_v1alpha3.types.Asset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = messages_pb2.ModifyAssetRequest(
            org_name=org_name,
            id=id_,
            add_or_update_marks=add_or_update_marks,
            remove_marks_with_keys=remove_marks_with_keys,
        )
        return self._modify_asset(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def search_findings(self,
                        org_name,
                        reference_time=None,
                        query=None,
                        order_by=None,
                        page_size=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Search findings within an organization.

        Example:
            >>> from google.cloud import securitycenter_v1alpha3
            >>>
            >>> client = securitycenter_v1alpha3.SecurityCenterClient()
            >>>
            >>> org_name = client.organization_path('[ORGANIZATION]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_findings(org_name):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.search_findings(org_name, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            org_name (str): The name of the organization to which the findings belong. Its format is
                \"organizations/[organization_id]\". For example, \"organizations/1234\".
            reference_time (Union[dict, ~google.cloud.securitycenter_v1alpha3.types.Timestamp]): The reference point used to determine the findings at a specific
                point in time.
                Queries with the timestamp in the future are rounded down to the
                current time on the server. If the value is not given, \"now\" is going to
                be used implicitly.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.securitycenter_v1alpha3.types.Timestamp`
            query (str): Expression that defines the query to apply across findings.
                The expression is a list of one or more restrictions combined via logical
                operators ``AND`` and ``OR``.
                Parentheses are supported, and in absence of parentheses ``OR`` has higher
                precedence than ``AND``.

                Restrictions have the form ``<field> <operator> <value>`` and may have a ``-``
                character in front of them to indicate negation. The fields can be of the
                following types:

                * Attribute - optional ``attribute.`` prefix or no prefix and name.
                * Property - mandatory ``property.`` prefix and name.
                * Mark - mandatory ``mark`` prefix and name.

                The supported operators are:

                * ``=`` for all value types.
                * ``>``, ``<``, ``>=``, ``<=`` for integer values.
                * ``:``, meaning substring matching, for strings.

                The supported value types are:

                * string literals in quotes.
                * integer literals without quotes.
                * boolean literals ``true`` and ``false`` without quotes.

                For example, ``property.count = 100`` is a valid query string.
            order_by (str): Expression that defines what fields and order to use for sorting.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.securitycenter_v1alpha3.types.Finding` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = messages_pb2.SearchFindingsRequest(
            org_name=org_name,
            reference_time=reference_time,
            query=query,
            order_by=order_by,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._search_findings,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='findings',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def create_finding(self,
                       org_name,
                       source_finding,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Creates a finding, creating the same finding with a later event_time will
        update the existing one. CSCC provides the capability for users to search
        findings based on timestamps.

        Example:
            >>> from google.cloud import securitycenter_v1alpha3
            >>>
            >>> client = securitycenter_v1alpha3.SecurityCenterClient()
            >>>
            >>> org_name = client.organization_path('[ORGANIZATION]')
            >>>
            >>> # TODO: Initialize ``source_finding``:
            >>> source_finding = {}
            >>>
            >>> response = client.create_finding(org_name, source_finding)

        Args:
            org_name (str): Name of the organization to search for assets. Its format is
                \"organizations/[organization_id]\". For example, \"organizations/1234\".
            source_finding (Union[dict, ~google.cloud.securitycenter_v1alpha3.types.SourceFinding]): The source finding to be created.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.securitycenter_v1alpha3.types.SourceFinding`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.securitycenter_v1alpha3.types.Finding` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = messages_pb2.CreateFindingRequest(
            org_name=org_name,
            source_finding=source_finding,
        )
        return self._create_finding(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def modify_finding(self,
                       org_name,
                       id_,
                       add_or_update_marks=None,
                       remove_marks_with_keys=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Provides a way for users to update mutable parts of a given finding.
        Modifies marks on a finding.

        Example:
            >>> from google.cloud import securitycenter_v1alpha3
            >>>
            >>> client = securitycenter_v1alpha3.SecurityCenterClient()
            >>>
            >>> org_name = client.organization_path('[ORGANIZATION]')
            >>>
            >>> # TODO: Initialize ``id_``:
            >>> id_ = ''
            >>>
            >>> response = client.modify_finding(org_name, id_)

        Args:
            org_name (str): Organization name.
            id_ (str): Id of the finding.
            add_or_update_marks (dict[str -> str]): Keys and values to add/update on the finding.
                If a mark with the same key already exists, its value will be replaced by
                the updated value.
            remove_marks_with_keys (list[str]): A list of keys defining the marks to remove from the finding. There can be
                no overlaps between keys to remove and keys to add or update.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.securitycenter_v1alpha3.types.Finding` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = messages_pb2.ModifyFindingRequest(
            org_name=org_name,
            id=id_,
            add_or_update_marks=add_or_update_marks,
            remove_marks_with_keys=remove_marks_with_keys,
        )
        return self._modify_finding(
            request, retry=retry, timeout=timeout, metadata=metadata)

// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Note: this file is purely for documentation. Any contents are not expected
// to be loaded as the JS file.

/**
 * Representation of a Google Cloud Platform asset. Examples of assets include:
 * App Engine Application, Project, Bucket, etc.
 *
 * @property {string} id
 *   Unique identifier for this asset. This identifier persists following
 *   modification/deletion/recreation.
 *
 * @property {string} parentId
 *   Unique identifier for this asset's parent. For example, a Project's parent
 *   would be either the organization it belongs to OR the folder it resides in.
 *
 * @property {string} type
 *   The type of asset. Examples include: APPLICATION, PROJECT, ORGANIZATION,
 *   etc.
 *
 * @property {string[]} owners
 *   Owners of the asset. Commonly represented as email addresses.
 *
 * @property {Object} updateTime
 *   The time at which the asset has been last updated, added or deleted in
 *   CSCC.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @property {number} state
 *   State of the asset.
 *
 *   The number should be among the values of [State]{@link google.cloud.securitycenter.v1alpha3.State}
 *
 * @property {Object} properties
 *   Properties associated with the asset.
 *
 *   This object should have the same structure as [Struct]{@link google.protobuf.Struct}
 *
 * @property {Object.<string, string>} marks
 *   User specified marks placed on the asset.
 *
 * @typedef Asset
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.Asset definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var Asset = {
  // This is for documentation. Actual contents will be loaded by gRPC.

  /**
   * State of the asset.
   *
   * When querying across two points in time this describes
   * the change between the two points: NOT_FOUND, ADDED, REMOVED, or
   * ACTIVE_AT_BOTH.
   *
   * When querying for a single point in time this describes the
   * state at that time: NOT_FOUND, ACTIVE, REMOVED.
   *
   * @enum {number}
   * @memberof google.cloud.securitycenter.v1alpha3
   */
  State: {

    /**
     * Invalid state.
     */
    STATE_UNSPECIFIED: 0,

    /**
     * Asset was active for the point in time.
     */
    ACTIVE: 1,

    /**
     * Asset was not found for the point(s) in time.
     */
    NOT_FOUND: 2,

    /**
     * Asset was added between the points in time.
     */
    ADDED: 3,

    /**
     * Asset was removed between the points in time.
     */
    REMOVED: 4,

    /**
     * Asset was active at both point(s) in time.
     */
    ACTIVE_AT_BOTH: 5
  }
};

/**
 * Representation of a scanner's finding.
 *
 * @property {string} id
 *   Unique identifier for this finding. The same finding and identifier can
 *   appear at multiple points in time.
 *
 * @property {string} assetId
 *   Unique identifier for the asset the finding relates to.
 *
 * @property {string} scannerId
 *   Unique identifier for the scanner that produced the finding.
 *
 * @property {Object} updateTime
 *   Time at which this finding was last updated. This does not include updates
 *   on user specified marks.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @property {Object} properties
 *   Properties associated with the finding.
 *
 *   This object should have the same structure as [Struct]{@link google.protobuf.Struct}
 *
 * @property {Object.<string, string>} marks
 *   User specified marks placed on the finding.
 *
 * @typedef Finding
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.Finding definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var Finding = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Representation of a source's finding.
 *
 * @property {string} id
 *   Required field, an organization & source unique immutable identifier
 *   provided by the sources.
 *
 * @property {string} category
 *   Required field, category of a finding, this is a custom string field. In
 *   general, sources have logical groupings for their findings. For example,
 *   the Data Loss Prevention Scanner has the following types: "SSN",
 *   "US passport", "credit card number" etc. This field is indexed and used by
 *   CSCC frontend for data visualization. It's also useful for reporting and
 *   analysis. It's recommended to populate this field consistently.
 *
 * @property {string[]} assetIds
 *   Required field, list of ids of affected assets. These ids should strictly
 *   map to one of the existing asset ids in the asset inventory for the
 *   orgnanization, which is populated by CSCC backend, not meeting any of the
 *   aforementioned conditions would result in NOT_FOUND error. Asset types must
 *   be supported by CSCC and it's recommended to pick the most granular asset
 *   type, e.g if a file in a VM instance is affected, asset id of the VM
 *   instance should be provided since file is not a supported asset type in
 *   CSCC and project id is too broad.
 *
 * @property {string} sourceId
 *   Required field, ID of the finding source, a source is a producer of
 *   security findings, source ids are namespaced under each organization. For
 *   Google integrated sources, please use their official source ids for better
 *   FE integration. For custom sources, choose an id that's not in conflict
 *   with any existing ones.
 *
 * @property {Object} eventTime
 *   Time when the finding was generated by the source.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @property {string} url
 *   A https url provided by the source for users to click on to see more
 *   information, used for UI navigation.
 *
 * @property {Object} properties
 *   Key-value pairs provided by the source. Indexing will be provided
 *   for each key.
 *
 *   This object should have the same structure as [Struct]{@link google.protobuf.Struct}
 *
 * @property {Object} attributes
 *   Dynamically calculated attributes provided by us.
 *   e.g first_discovered, create_time.
 *   Note: This field is used in responses only. Any value specified here in a
 *   request is ignored.
 *
 *   This object should have the same structure as [Struct]{@link google.protobuf.Struct}
 *
 * @property {Object.<string, string>} marks
 *   User specified marks placed on the finding.
 *   Note: This field is used in responses only. Any value specified here in a
 *   request is ignored.
 *
 * @typedef SourceFinding
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.SourceFinding definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var SourceFinding = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Request message for CreatingFinding.
 *
 * @property {string} orgName
 *   Name of the organization to search for assets. Its format is
 *   "organizations/[organization_id]". For example, "organizations/1234".
 *
 * @property {Object} sourceFinding
 *   The source finding to be created.
 *
 *   This object should have the same structure as [SourceFinding]{@link google.cloud.securitycenter.v1alpha3.SourceFinding}
 *
 * @typedef CreateFindingRequest
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.CreateFindingRequest definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var CreateFindingRequest = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Request message for ModifyFinding.
 *
 * @property {string} orgName
 *   Organization name.
 *
 * @property {string} id
 *   Id of the finding.
 *
 * @property {Object.<string, string>} addOrUpdateMarks
 *   Keys and values to add/update on the finding.
 *   If a mark with the same key already exists, its value will be replaced by
 *   the updated value.
 *
 * @property {string[]} removeMarksWithKeys
 *   A list of keys defining the marks to remove from the finding. There can be
 *   no overlaps between keys to remove and keys to add or update.
 *
 * @typedef ModifyFindingRequest
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.ModifyFindingRequest definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var ModifyFindingRequest = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Request message for SearchAssets.
 *
 * @property {string} orgName
 *   Name of the organization to search for assets. Its format is
 *   "organizations/[organization_id]". For example, "organizations/1234".
 *
 * @property {string} query
 *   Expression that defines the query to apply across assets.
 *   The expression is a list of one or more restrictions combined via logical
 *   operators `AND` and `OR`.
 *   Parentheses are not supported, and `OR` has higher precedence than `AND`.
 *
 *   Restrictions have the form `<field> <operator> <value>` and may have a `-`
 *   character in front of them to indicate negation. The fields can be of the
 *   following types:
 *
 *   * Attribute: optional `attribute.` prefix or no prefix and name.
 *   * Property: mandatory `property.` prefix and name.
 *   * Mark: mandatory `mark` prefix and name.
 *
 *   The supported operators are:
 *
 *   * `=` for all value types.
 *   * `>`, `<`, `>=`, `<=` for integer values.
 *   * `:`, meaning substring matching, for strings.
 *
 *   The supported value types are:
 *
 *   * string literals in quotes.
 *   * integer literals without quotes.
 *   * boolean literals `true` and `false` without quotes.
 *
 *   For example, `property.count = 100` is a valid query string.
 *
 * @property {string} orderBy
 *   Expression that defines what fields and order to use for sorting.
 *
 * @property {Object} referenceTime
 *   Time at which to search for assets. The search will capture the state of
 *   assets at this point in time.
 *
 *   Not providing a value or providing one in the future is treated as current.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @property {Object} compareDuration
 *   When compare_duration is set, the Asset's "state" attribute is updated to
 *   indicate whether the asset was added, removed, or remained present during
 *   the compare_duration period of time that precedes the reference_time. This
 *   is the time between (reference_time - compare_duration) and reference_time.
 *
 *   The state value is derived based on the presence of the asset at the two
 *   points in time. Intermediate state changes between the two times don't
 *   affect the result. For example, the results aren't affected if the asset is
 *   removed and re-created again.
 *
 *   Possible "state" values when compare_duration is specified:
 *
 *   * "ADDED": indicates that the asset was not present before
 *                compare_duration, but present at reference_time.
 *   * "REMOVED": indicates that the asset was present at the start of
 *                compare_duration, but not present at reference_time.
 *   * "ACTIVE_AT_BOTH": indicates that the asset was present at both the
 *                start and the end of the time period defined by
 *                compare_duration and reference_time.
 *
 *   If compare_duration is not specified, then the only possible state is
 *   "ACTIVE", which indicates that the asset is present at reference_time.
 *
 *   This object should have the same structure as [Duration]{@link google.protobuf.Duration}
 *
 * @property {string} pageToken
 *   Optional pagination token returned in an earlier call.
 *
 * @property {number} pageSize
 *   The maximum number of results to return in a single response.
 *
 * @typedef SearchAssetsRequest
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.SearchAssetsRequest definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var SearchAssetsRequest = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Response message for SearchAssets.
 *
 * @property {Object[]} assets
 *   Assets returned by the request.
 *
 *   This object should have the same structure as [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset}
 *
 * @property {string} nextPageToken
 *   Token to retrieve the next page of results, or empty if there are no more
 *   results.
 *
 * @property {number} totalSize
 *   The total number of results available.
 *
 * @property {Object} referenceTime
 *   Time provided for reference_time in the request.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @property {Object} compareDuration
 *   Time provided for compare_duration in the request.
 *
 *   This object should have the same structure as [Duration]{@link google.protobuf.Duration}
 *
 * @typedef SearchAssetsResponse
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.SearchAssetsResponse definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var SearchAssetsResponse = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Request message for SearchFindings.
 *
 * @property {string} orgName
 *   The name of the organization to which the findings belong. Its format is
 *   "organizations/[organization_id]". For example, "organizations/1234".
 *
 * @property {Object} referenceTime
 *   The reference point used to determine the findings at a specific
 *   point in time.
 *   Queries with the timestamp in the future are rounded down to the
 *   current time on the server. If the value is not given, "now" is going to
 *   be used implicitly.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @property {string} query
 *   Expression that defines the query to apply across findings.
 *   The expression is a list of one or more restrictions combined via logical
 *   operators `AND` and `OR`.
 *   Parentheses are supported, and in absence of parentheses `OR` has higher
 *   precedence than `AND`.
 *
 *   Restrictions have the form `<field> <operator> <value>` and may have a `-`
 *   character in front of them to indicate negation. The fields can be of the
 *   following types:
 *
 *   * Attribute - optional `attribute.` prefix or no prefix and name.
 *   * Property - mandatory `property.` prefix and name.
 *   * Mark - mandatory `mark` prefix and name.
 *
 *   The supported operators are:
 *
 *   * `=` for all value types.
 *   * `>`, `<`, `>=`, `<=` for integer values.
 *   * `:`, meaning substring matching, for strings.
 *
 *   The supported value types are:
 *
 *   * string literals in quotes.
 *   * integer literals without quotes.
 *   * boolean literals `true` and `false` without quotes.
 *
 *   For example, `property.count = 100` is a valid query string.
 *
 * @property {string} orderBy
 *   Expression that defines what fields and order to use for sorting.
 *
 * @property {string} pageToken
 *   Optional pagination token returned in an earlier call.
 *
 * @property {number} pageSize
 *   The maximum number of results to return.
 *
 * @typedef SearchFindingsRequest
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.SearchFindingsRequest definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var SearchFindingsRequest = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Response message for SearchFindings.
 *
 * @property {Object[]} findings
 *   Findings returned by the request.
 *
 *   This object should have the same structure as [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}
 *
 * @property {string} nextPageToken
 *   Token to retrieve the next page of results, or empty if there are no more
 *   results.
 *
 * @property {number} totalSize
 *   The total number of findings irrespective of pagination.
 *
 * @property {Object} referenceTime
 *   Time provided for reference_time in the request.
 *
 *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
 *
 * @typedef SearchFindingsResponse
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.SearchFindingsResponse definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var SearchFindingsResponse = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * Request message for modifying the marks on an asset.
 *
 * @property {string} orgName
 *   Organization name.
 *
 * @property {string} id
 *   Unique identifier for the asset to be modified.
 *
 * @property {Object.<string, string>} addOrUpdateMarks
 *   Keys and values to add/update on the asset.
 *
 *   If a mark with the same key already exists, its value will be replaced by
 *   the updated value.
 *
 * @property {string[]} removeMarksWithKeys
 *   A list of keys defining the marks to remove from the asset. There can be no
 *   overlaps between keys to remove and keys to add or update.
 *
 * @typedef ModifyAssetRequest
 * @memberof google.cloud.securitycenter.v1alpha3
 * @see [google.cloud.securitycenter.v1alpha3.ModifyAssetRequest definition in proto format]{@link https://github.com/googleapis/googleapis/blob/master/google/cloud/securitycenter/v1alpha3/messages.proto}
 */
var ModifyAssetRequest = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};
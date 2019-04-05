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

'use strict';

const gapicConfig = require('./security_center_client_config');
const gax = require('google-gax');
const merge = require('lodash.merge');
const path = require('path');

const VERSION = require('../../package.json').version;

/**
 * Service for Cloud Security Command Center.
 *
 * @class
 * @memberof v1alpha3
 */
class SecurityCenterClient {
  /**
   * Construct an instance of SecurityCenterClient.
   *
   * @param {object} [options] - The configuration object. See the subsequent
   *   parameters for more details.
   * @param {object} [options.credentials] - Credentials object.
   * @param {string} [options.credentials.client_email]
   * @param {string} [options.credentials.private_key]
   * @param {string} [options.email] - Account email address. Required when
   *     using a .pem or .p12 keyFilename.
   * @param {string} [options.keyFilename] - Full path to the a .json, .pem, or
   *     .p12 key downloaded from the Google Developers Console. If you provide
   *     a path to a JSON file, the projectId option below is not necessary.
   *     NOTE: .pem and .p12 require you to specify options.email as well.
   * @param {number} [options.port] - The port on which to connect to
   *     the remote host.
   * @param {string} [options.projectId] - The project ID from the Google
   *     Developer's Console, e.g. 'grape-spaceship-123'. We will also check
   *     the environment variable GCLOUD_PROJECT for your project ID. If your
   *     app is running in an environment which supports
   *     {@link https://developers.google.com/identity/protocols/application-default-credentials Application Default Credentials},
   *     your project ID will be detected automatically.
   * @param {function} [options.promise] - Custom promise module to use instead
   *     of native Promises.
   * @param {string} [options.servicePath] - The domain name of the
   *     API remote host.
   */
  constructor(opts) {
    this._descriptors = {};

    // Ensure that options include the service address and port.
    opts = Object.assign(
      {
        clientConfig: {},
        port: this.constructor.port,
        servicePath: this.constructor.servicePath,
      },
      opts
    );

    // Create a `gaxGrpc` object, with any grpc-specific options
    // sent to the client.
    opts.scopes = this.constructor.scopes;
    var gaxGrpc = gax.grpc(opts);

    // Save the auth object to the client, for use by other methods.
    this.auth = gaxGrpc.auth;

    // Determine the client header string.
    var clientHeader = [
      `gl-node/${process.version.node}`,
      `grpc/${gaxGrpc.grpcVersion}`,
      `gax/${gax.version}`,
      `gapic/${VERSION}`,
    ];
    if (opts.libName && opts.libVersion) {
      clientHeader.push(`${opts.libName}/${opts.libVersion}`);
    }

    // Load the applicable protos.
    var protos = merge(
      {},
      gaxGrpc.loadProto(
        path.join(__dirname, '..', '..', 'protos'),
        'google/cloud/securitycenter/v1alpha3/services.proto'
      )
    );

    // This API contains "path templates"; forward-slash-separated
    // identifiers to uniquely identify resources within the API.
    // Create useful helper objects for these.
    this._pathTemplates = {
      organizationPathTemplate: new gax.PathTemplate(
        'organizations/{organization}'
      ),
    };

    // Some of the methods on this service return "paged" results,
    // (e.g. 50 results at a time, with tokens to get subsequent
    // pages). Denote the keys used for pagination and results.
    this._descriptors.page = {
      searchAssets: new gax.PageDescriptor(
        'pageToken',
        'nextPageToken',
        'assets'
      ),
      searchFindings: new gax.PageDescriptor(
        'pageToken',
        'nextPageToken',
        'findings'
      ),
    };

    // Put together the default options sent with requests.
    var defaults = gaxGrpc.constructSettings(
      'google.cloud.securitycenter.v1alpha3.SecurityCenter',
      gapicConfig,
      opts.clientConfig,
      {'x-goog-api-client': clientHeader.join(' ')}
    );

    // Set up a dictionary of "inner API calls"; the core implementation
    // of calling the API is handled in `google-gax`, with this code
    // merely providing the destination and request information.
    this._innerApiCalls = {};

    // Put together the "service stub" for
    // google.cloud.securitycenter.v1alpha3.SecurityCenter.
    var securityCenterStub = gaxGrpc.createStub(
      protos.google.cloud.securitycenter.v1alpha3.SecurityCenter,
      opts
    );

    // Iterate over each of the methods that the service provides
    // and create an API call method for each.
    var securityCenterStubMethods = [
      'searchAssets',
      'modifyAsset',
      'searchFindings',
      'createFinding',
      'modifyFinding',
    ];
    for (let methodName of securityCenterStubMethods) {
      this._innerApiCalls[methodName] = gax.createApiCall(
        securityCenterStub.then(
          stub =>
            function() {
              var args = Array.prototype.slice.call(arguments, 0);
              return stub[methodName].apply(stub, args);
            }
        ),
        defaults[methodName],
        this._descriptors.page[methodName]
      );
    }
  }

  /**
   * The DNS address for this API service.
   */
  static get servicePath() {
    return 'securitycenter.googleapis.com';
  }

  /**
   * The port for this API service.
   */
  static get port() {
    return 443;
  }

  /**
   * The scopes needed to make gRPC calls for every method defined
   * in this service.
   */
  static get scopes() {
    return [
      'https://www.googleapis.com/auth/cloud-platform',
    ];
  }

  /**
   * Return the project ID used by this class.
   * @param {function(Error, string)} callback - the callback to
   *   be called with the current project Id.
   */
  getProjectId(callback) {
    return this.auth.getProjectId(callback);
  }

  // -------------------
  // -- Service calls --
  // -------------------

  /**
   * Search assets within an organization.
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   Name of the organization to search for assets. Its format is
   *   "organizations/[organization_id]". For example, "organizations/1234".
   * @param {string} [request.query]
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
   * @param {string} [request.orderBy]
   *   Expression that defines what fields and order to use for sorting.
   * @param {Object} [request.referenceTime]
   *   Time at which to search for assets. The search will capture the state of
   *   assets at this point in time.
   *
   *   Not providing a value or providing one in the future is treated as current.
   *
   *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
   * @param {Object} [request.compareDuration]
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
   * @param {number} [request.pageSize]
   *   The maximum number of resources contained in the underlying API
   *   response. If page streaming is performed per-resource, this
   *   parameter does not affect the return value. If page streaming is
   *   performed per-page, this determines the maximum number of
   *   resources in a page.
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @param {function(?Error, ?Array, ?Object, ?Object)} [callback]
   *   The function which will be called with the result of the API call.
   *
   *   The second parameter to the callback is Array of [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset}.
   *
   *   When autoPaginate: false is specified through options, it contains the result
   *   in a single response. If the response indicates the next page exists, the third
   *   parameter is set to be used for the next request object. The fourth parameter keeps
   *   the raw response object of an object representing [SearchAssetsResponse]{@link google.cloud.securitycenter.v1alpha3.SearchAssetsResponse}.
   * @returns {Promise} - The promise which resolves to an array.
   *   The first element of the array is Array of [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset}.
   *
   *   When autoPaginate: false is specified through options, the array has three elements.
   *   The first element is Array of [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset} in a single response.
   *   The second element is the next request object if the response
   *   indicates the next page exists, or null. The third element is
   *   an object representing [SearchAssetsResponse]{@link google.cloud.securitycenter.v1alpha3.SearchAssetsResponse}.
   *
   *   The promise has a method named "cancel" which cancels the ongoing API call.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * // Iterate over all elements.
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   *
   * client.searchAssets({orgName: formattedOrgName})
   *   .then(responses => {
   *     var resources = responses[0];
   *     for (let i = 0; i < resources.length; i += 1) {
   *       // doThingsWith(resources[i])
   *     }
   *   })
   *   .catch(err => {
   *     console.error(err);
   *   });
   *
   * // Or obtain the paged response.
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   *
   *
   * var options = {autoPaginate: false};
   * var callback = responses => {
   *   // The actual resources in a response.
   *   var resources = responses[0];
   *   // The next request if the response shows that there are more responses.
   *   var nextRequest = responses[1];
   *   // The actual response object, if necessary.
   *   // var rawResponse = responses[2];
   *   for (let i = 0; i < resources.length; i += 1) {
   *     // doThingsWith(resources[i]);
   *   }
   *   if (nextRequest) {
   *     // Fetch the next page.
   *     return client.searchAssets(nextRequest, options).then(callback);
   *   }
   * }
   * client.searchAssets({orgName: formattedOrgName}, options)
   *   .then(callback)
   *   .catch(err => {
   *     console.error(err);
   *   });
   */
  searchAssets(request, options, callback) {
    if (options instanceof Function && callback === undefined) {
      callback = options;
      options = {};
    }
    options = options || {};

    return this._innerApiCalls.searchAssets(request, options, callback);
  }

  /**
   * Equivalent to {@link searchAssets}, but returns a NodeJS Stream object.
   *
   * This fetches the paged responses for {@link searchAssets} continuously
   * and invokes the callback registered for 'data' event for each element in the
   * responses.
   *
   * The returned object has 'end' method when no more elements are required.
   *
   * autoPaginate option will be ignored.
   *
   * @see {@link https://nodejs.org/api/stream.html}
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   Name of the organization to search for assets. Its format is
   *   "organizations/[organization_id]". For example, "organizations/1234".
   * @param {string} [request.query]
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
   * @param {string} [request.orderBy]
   *   Expression that defines what fields and order to use for sorting.
   * @param {Object} [request.referenceTime]
   *   Time at which to search for assets. The search will capture the state of
   *   assets at this point in time.
   *
   *   Not providing a value or providing one in the future is treated as current.
   *
   *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
   * @param {Object} [request.compareDuration]
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
   * @param {number} [request.pageSize]
   *   The maximum number of resources contained in the underlying API
   *   response. If page streaming is performed per-resource, this
   *   parameter does not affect the return value. If page streaming is
   *   performed per-page, this determines the maximum number of
   *   resources in a page.
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @returns {Stream}
   *   An object stream which emits an object representing [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset} on 'data' event.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   * client.searchAssetsStream({orgName: formattedOrgName})
   *   .on('data', element => {
   *     // doThingsWith(element)
   *   }).on('error', err => {
   *     console.log(err);
   *   });
   */
  searchAssetsStream(request, options) {
    options = options || {};

    return this._descriptors.page.searchAssets.createStream(
      this._innerApiCalls.searchAssets,
      request,
      options
    );
  };

  /**
   * Modifies the marks on the specified asset.
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   Organization name.
   * @param {string} request.id
   *   Unique identifier for the asset to be modified.
   * @param {Object.<string, string>} [request.addOrUpdateMarks]
   *   Keys and values to add/update on the asset.
   *
   *   If a mark with the same key already exists, its value will be replaced by
   *   the updated value.
   * @param {string[]} [request.removeMarksWithKeys]
   *   A list of keys defining the marks to remove from the asset. There can be no
   *   overlaps between keys to remove and keys to add or update.
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @param {function(?Error, ?Object)} [callback]
   *   The function which will be called with the result of the API call.
   *
   *   The second parameter to the callback is an object representing [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset}.
   * @returns {Promise} - The promise which resolves to an array.
   *   The first element of the array is an object representing [Asset]{@link google.cloud.securitycenter.v1alpha3.Asset}.
   *   The promise has a method named "cancel" which cancels the ongoing API call.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   * var id = '';
   * var request = {
   *   orgName: formattedOrgName,
   *   id: id,
   * };
   * client.modifyAsset(request)
   *   .then(responses => {
   *     var response = responses[0];
   *     // doThingsWith(response)
   *   })
   *   .catch(err => {
   *     console.error(err);
   *   });
   */
  modifyAsset(request, options, callback) {
    if (options instanceof Function && callback === undefined) {
      callback = options;
      options = {};
    }
    options = options || {};

    return this._innerApiCalls.modifyAsset(request, options, callback);
  }

  /**
   * Search findings within an organization.
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   The name of the organization to which the findings belong. Its format is
   *   "organizations/[organization_id]". For example, "organizations/1234".
   * @param {Object} [request.referenceTime]
   *   The reference point used to determine the findings at a specific
   *   point in time.
   *   Queries with the timestamp in the future are rounded down to the
   *   current time on the server. If the value is not given, "now" is going to
   *   be used implicitly.
   *
   *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
   * @param {string} [request.query]
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
   * @param {string} [request.orderBy]
   *   Expression that defines what fields and order to use for sorting.
   * @param {number} [request.pageSize]
   *   The maximum number of resources contained in the underlying API
   *   response. If page streaming is performed per-resource, this
   *   parameter does not affect the return value. If page streaming is
   *   performed per-page, this determines the maximum number of
   *   resources in a page.
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @param {function(?Error, ?Array, ?Object, ?Object)} [callback]
   *   The function which will be called with the result of the API call.
   *
   *   The second parameter to the callback is Array of [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}.
   *
   *   When autoPaginate: false is specified through options, it contains the result
   *   in a single response. If the response indicates the next page exists, the third
   *   parameter is set to be used for the next request object. The fourth parameter keeps
   *   the raw response object of an object representing [SearchFindingsResponse]{@link google.cloud.securitycenter.v1alpha3.SearchFindingsResponse}.
   * @returns {Promise} - The promise which resolves to an array.
   *   The first element of the array is Array of [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}.
   *
   *   When autoPaginate: false is specified through options, the array has three elements.
   *   The first element is Array of [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding} in a single response.
   *   The second element is the next request object if the response
   *   indicates the next page exists, or null. The third element is
   *   an object representing [SearchFindingsResponse]{@link google.cloud.securitycenter.v1alpha3.SearchFindingsResponse}.
   *
   *   The promise has a method named "cancel" which cancels the ongoing API call.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * // Iterate over all elements.
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   *
   * client.searchFindings({orgName: formattedOrgName})
   *   .then(responses => {
   *     var resources = responses[0];
   *     for (let i = 0; i < resources.length; i += 1) {
   *       // doThingsWith(resources[i])
   *     }
   *   })
   *   .catch(err => {
   *     console.error(err);
   *   });
   *
   * // Or obtain the paged response.
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   *
   *
   * var options = {autoPaginate: false};
   * var callback = responses => {
   *   // The actual resources in a response.
   *   var resources = responses[0];
   *   // The next request if the response shows that there are more responses.
   *   var nextRequest = responses[1];
   *   // The actual response object, if necessary.
   *   // var rawResponse = responses[2];
   *   for (let i = 0; i < resources.length; i += 1) {
   *     // doThingsWith(resources[i]);
   *   }
   *   if (nextRequest) {
   *     // Fetch the next page.
   *     return client.searchFindings(nextRequest, options).then(callback);
   *   }
   * }
   * client.searchFindings({orgName: formattedOrgName}, options)
   *   .then(callback)
   *   .catch(err => {
   *     console.error(err);
   *   });
   */
  searchFindings(request, options, callback) {
    if (options instanceof Function && callback === undefined) {
      callback = options;
      options = {};
    }
    options = options || {};

    return this._innerApiCalls.searchFindings(request, options, callback);
  }

  /**
   * Equivalent to {@link searchFindings}, but returns a NodeJS Stream object.
   *
   * This fetches the paged responses for {@link searchFindings} continuously
   * and invokes the callback registered for 'data' event for each element in the
   * responses.
   *
   * The returned object has 'end' method when no more elements are required.
   *
   * autoPaginate option will be ignored.
   *
   * @see {@link https://nodejs.org/api/stream.html}
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   The name of the organization to which the findings belong. Its format is
   *   "organizations/[organization_id]". For example, "organizations/1234".
   * @param {Object} [request.referenceTime]
   *   The reference point used to determine the findings at a specific
   *   point in time.
   *   Queries with the timestamp in the future are rounded down to the
   *   current time on the server. If the value is not given, "now" is going to
   *   be used implicitly.
   *
   *   This object should have the same structure as [Timestamp]{@link google.protobuf.Timestamp}
   * @param {string} [request.query]
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
   * @param {string} [request.orderBy]
   *   Expression that defines what fields and order to use for sorting.
   * @param {number} [request.pageSize]
   *   The maximum number of resources contained in the underlying API
   *   response. If page streaming is performed per-resource, this
   *   parameter does not affect the return value. If page streaming is
   *   performed per-page, this determines the maximum number of
   *   resources in a page.
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @returns {Stream}
   *   An object stream which emits an object representing [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding} on 'data' event.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   * client.searchFindingsStream({orgName: formattedOrgName})
   *   .on('data', element => {
   *     // doThingsWith(element)
   *   }).on('error', err => {
   *     console.log(err);
   *   });
   */
  searchFindingsStream(request, options) {
    options = options || {};

    return this._descriptors.page.searchFindings.createStream(
      this._innerApiCalls.searchFindings,
      request,
      options
    );
  };

  /**
   * Creates a finding, creating the same finding with a later event_time will
   * update the existing one. CSCC provides the capability for users to search
   * findings based on timestamps.
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   Name of the organization to search for assets. Its format is
   *   "organizations/[organization_id]". For example, "organizations/1234".
   * @param {Object} request.sourceFinding
   *   The source finding to be created.
   *
   *   This object should have the same structure as [SourceFinding]{@link google.cloud.securitycenter.v1alpha3.SourceFinding}
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @param {function(?Error, ?Object)} [callback]
   *   The function which will be called with the result of the API call.
   *
   *   The second parameter to the callback is an object representing [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}.
   * @returns {Promise} - The promise which resolves to an array.
   *   The first element of the array is an object representing [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}.
   *   The promise has a method named "cancel" which cancels the ongoing API call.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   * var sourceFinding = {};
   * var request = {
   *   orgName: formattedOrgName,
   *   sourceFinding: sourceFinding,
   * };
   * client.createFinding(request)
   *   .then(responses => {
   *     var response = responses[0];
   *     // doThingsWith(response)
   *   })
   *   .catch(err => {
   *     console.error(err);
   *   });
   */
  createFinding(request, options, callback) {
    if (options instanceof Function && callback === undefined) {
      callback = options;
      options = {};
    }
    options = options || {};

    return this._innerApiCalls.createFinding(request, options, callback);
  }

  /**
   * Provides a way for users to update mutable parts of a given finding.
   * Modifies marks on a finding.
   *
   * @param {Object} request
   *   The request object that will be sent.
   * @param {string} request.orgName
   *   Organization name.
   * @param {string} request.id
   *   Id of the finding.
   * @param {Object.<string, string>} [request.addOrUpdateMarks]
   *   Keys and values to add/update on the finding.
   *   If a mark with the same key already exists, its value will be replaced by
   *   the updated value.
   * @param {string[]} [request.removeMarksWithKeys]
   *   A list of keys defining the marks to remove from the finding. There can be
   *   no overlaps between keys to remove and keys to add or update.
   * @param {Object} [options]
   *   Optional parameters. You can override the default settings for this call, e.g, timeout,
   *   retries, paginations, etc. See [gax.CallOptions]{@link https://googleapis.github.io/gax-nodejs/global.html#CallOptions} for the details.
   * @param {function(?Error, ?Object)} [callback]
   *   The function which will be called with the result of the API call.
   *
   *   The second parameter to the callback is an object representing [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}.
   * @returns {Promise} - The promise which resolves to an array.
   *   The first element of the array is an object representing [Finding]{@link google.cloud.securitycenter.v1alpha3.Finding}.
   *   The promise has a method named "cancel" which cancels the ongoing API call.
   *
   * @example
   *
   * const securitycenter = require('securitycenter.v1alpha3');
   *
   * var client = new securitycenter.v1alpha3.SecurityCenterClient({
   *   // optional auth parameters.
   * });
   *
   * var formattedOrgName = client.organizationPath('[ORGANIZATION]');
   * var id = '';
   * var request = {
   *   orgName: formattedOrgName,
   *   id: id,
   * };
   * client.modifyFinding(request)
   *   .then(responses => {
   *     var response = responses[0];
   *     // doThingsWith(response)
   *   })
   *   .catch(err => {
   *     console.error(err);
   *   });
   */
  modifyFinding(request, options, callback) {
    if (options instanceof Function && callback === undefined) {
      callback = options;
      options = {};
    }
    options = options || {};

    return this._innerApiCalls.modifyFinding(request, options, callback);
  }

  // --------------------
  // -- Path templates --
  // --------------------

  /**
   * Return a fully-qualified organization resource name string.
   *
   * @param {String} organization
   * @returns {String}
   */
  organizationPath(organization) {
    return this._pathTemplates.organizationPathTemplate.render({
      organization: organization,
    });
  }

  /**
   * Parse the organizationName from a organization resource.
   *
   * @param {String} organizationName
   *   A fully-qualified path representing a organization resources.
   * @returns {String} - A string representing the organization.
   */
  matchOrganizationFromOrganizationName(organizationName) {
    return this._pathTemplates.organizationPathTemplate
      .match(organizationName)
      .organization;
  }
}


module.exports = SecurityCenterClient;

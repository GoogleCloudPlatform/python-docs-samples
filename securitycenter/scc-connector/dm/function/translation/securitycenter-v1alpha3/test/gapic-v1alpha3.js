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

const assert = require('assert');

const securitycenterModule = require('../src');

var FAKE_STATUS_CODE = 1;
var error = new Error();
error.code = FAKE_STATUS_CODE;

describe('SecurityCenterClient', () => {
  describe('searchAssets', () => {
    it('invokes searchAssets without error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var request = {
        orgName: formattedOrgName,
      };

      // Mock response
      var nextPageToken = '';
      var totalSize = 705419236;
      var assetsElement = {};
      var assets = [assetsElement];
      var expectedResponse = {
        nextPageToken: nextPageToken,
        totalSize: totalSize,
        assets: assets,
      };

      // Mock Grpc layer
      client._innerApiCalls.searchAssets = (actualRequest, options, callback) => {
        assert.deepStrictEqual(actualRequest, request);
        callback(null, expectedResponse.assets);
      };

      client.searchAssets(request, (err, response) => {
        assert.ifError(err);
        assert.deepStrictEqual(response, expectedResponse.assets);
        done();
      });
    });

    it('invokes searchAssets with error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var request = {
        orgName: formattedOrgName,
      };

      // Mock Grpc layer
      client._innerApiCalls.searchAssets = mockSimpleGrpcMethod(
        request,
        null,
        error
      );

      client.searchAssets(request, (err, response) => {
        assert(err instanceof Error);
        assert.equal(err.code, FAKE_STATUS_CODE);
        assert(typeof response === 'undefined');
        done();
      });
    });
  });

  describe('modifyAsset', () => {
    it('invokes modifyAsset without error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var id = 'id3355';
      var request = {
        orgName: formattedOrgName,
        id: id,
      };

      // Mock response
      var id2 = 'id23227150';
      var parentId = 'parentId2070327504';
      var type = 'type3575610';
      var expectedResponse = {
        id: id2,
        parentId: parentId,
        type: type,
      };

      // Mock Grpc layer
      client._innerApiCalls.modifyAsset = mockSimpleGrpcMethod(
        request,
        expectedResponse
      );

      client.modifyAsset(request, (err, response) => {
        assert.ifError(err);
        assert.deepStrictEqual(response, expectedResponse);
        done();
      });
    });

    it('invokes modifyAsset with error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var id = 'id3355';
      var request = {
        orgName: formattedOrgName,
        id: id,
      };

      // Mock Grpc layer
      client._innerApiCalls.modifyAsset = mockSimpleGrpcMethod(
        request,
        null,
        error
      );

      client.modifyAsset(request, (err, response) => {
        assert(err instanceof Error);
        assert.equal(err.code, FAKE_STATUS_CODE);
        assert(typeof response === 'undefined');
        done();
      });
    });
  });

  describe('searchFindings', () => {
    it('invokes searchFindings without error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var request = {
        orgName: formattedOrgName,
      };

      // Mock response
      var nextPageToken = '';
      var totalSize = 705419236;
      var findingsElement = {};
      var findings = [findingsElement];
      var expectedResponse = {
        nextPageToken: nextPageToken,
        totalSize: totalSize,
        findings: findings,
      };

      // Mock Grpc layer
      client._innerApiCalls.searchFindings = (actualRequest, options, callback) => {
        assert.deepStrictEqual(actualRequest, request);
        callback(null, expectedResponse.findings);
      };

      client.searchFindings(request, (err, response) => {
        assert.ifError(err);
        assert.deepStrictEqual(response, expectedResponse.findings);
        done();
      });
    });

    it('invokes searchFindings with error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var request = {
        orgName: formattedOrgName,
      };

      // Mock Grpc layer
      client._innerApiCalls.searchFindings = mockSimpleGrpcMethod(
        request,
        null,
        error
      );

      client.searchFindings(request, (err, response) => {
        assert(err instanceof Error);
        assert.equal(err.code, FAKE_STATUS_CODE);
        assert(typeof response === 'undefined');
        done();
      });
    });
  });

  describe('createFinding', () => {
    it('invokes createFinding without error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var sourceFinding = {};
      var request = {
        orgName: formattedOrgName,
        sourceFinding: sourceFinding,
      };

      // Mock response
      var id = 'id3355';
      var assetId = 'assetId-373202742';
      var scannerId = 'scannerId-332541188';
      var expectedResponse = {
        id: id,
        assetId: assetId,
        scannerId: scannerId,
      };

      // Mock Grpc layer
      client._innerApiCalls.createFinding = mockSimpleGrpcMethod(
        request,
        expectedResponse
      );

      client.createFinding(request, (err, response) => {
        assert.ifError(err);
        assert.deepStrictEqual(response, expectedResponse);
        done();
      });
    });

    it('invokes createFinding with error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var sourceFinding = {};
      var request = {
        orgName: formattedOrgName,
        sourceFinding: sourceFinding,
      };

      // Mock Grpc layer
      client._innerApiCalls.createFinding = mockSimpleGrpcMethod(
        request,
        null,
        error
      );

      client.createFinding(request, (err, response) => {
        assert(err instanceof Error);
        assert.equal(err.code, FAKE_STATUS_CODE);
        assert(typeof response === 'undefined');
        done();
      });
    });
  });

  describe('modifyFinding', () => {
    it('invokes modifyFinding without error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var id = 'id3355';
      var request = {
        orgName: formattedOrgName,
        id: id,
      };

      // Mock response
      var id2 = 'id23227150';
      var assetId = 'assetId-373202742';
      var scannerId = 'scannerId-332541188';
      var expectedResponse = {
        id: id2,
        assetId: assetId,
        scannerId: scannerId,
      };

      // Mock Grpc layer
      client._innerApiCalls.modifyFinding = mockSimpleGrpcMethod(
        request,
        expectedResponse
      );

      client.modifyFinding(request, (err, response) => {
        assert.ifError(err);
        assert.deepStrictEqual(response, expectedResponse);
        done();
      });
    });

    it('invokes modifyFinding with error', done => {
      var client = new securitycenterModule.v1alpha3.SecurityCenterClient({
        credentials: {client_email: 'bogus', private_key: 'bogus'},
        projectId: 'bogus',
      });

      // Mock request
      var formattedOrgName = client.organizationPath('[ORGANIZATION]');
      var id = 'id3355';
      var request = {
        orgName: formattedOrgName,
        id: id,
      };

      // Mock Grpc layer
      client._innerApiCalls.modifyFinding = mockSimpleGrpcMethod(
        request,
        null,
        error
      );

      client.modifyFinding(request, (err, response) => {
        assert(err instanceof Error);
        assert.equal(err.code, FAKE_STATUS_CODE);
        assert(typeof response === 'undefined');
        done();
      });
    });
  });

});

function mockSimpleGrpcMethod(expectedRequest, response, error) {
  return function(actualRequest, options, callback) {
    assert.deepStrictEqual(actualRequest, expectedRequest);
    if (error) {
      callback(error);
    } else if (response) {
      callback(null, response);
    } else {
      callback(null);
    }
  };
}

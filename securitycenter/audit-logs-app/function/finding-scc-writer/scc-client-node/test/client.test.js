'use strict'

// imports
const chai = require('chai')
const uuid4 = require('uuid4')
const chaiAsPromised = require('chai-as-promised')
const fs = require('fs')
const { Client } = require('../src/client')

// constants
const ACCOUNT_KEY_FILE = process.env.ACCOUNT_KEY_FILE
const ORGANIZATION_ID = process.env.ORGANIZATION_ID
const API_KEY = process.env.API_KEY

// use chai-as-promised
chai.use(chaiAsPromised)

// test only with right environment variables
const testIf = !ORGANIZATION_ID || !API_KEY || !fs.existsSync(ACCOUNT_KEY_FILE) ? test.skip : test

describe('SCC Rest Client', function () {
    beforeAll(() => {
        console.assert(ORGANIZATION_ID, 'Please set the ORGANIZATION_ID as environment variable')
        console.assert(API_KEY, 'Please set the API_KEY as environment variable')
        console.assert(fs.existsSync(ACCOUNT_KEY_FILE), 'Please set the ACCOUNT_KEY_FILE as environment variable')
    })

    describe('when calling the searchAssets', function () {
        testIf('should return all assets from organization using filter', function () {
            // given
            let client = new Client(ACCOUNT_KEY_FILE, ORGANIZATION_ID, API_KEY)
            let filter = 'security_center_properties.resource_type : "Project"'

            // when
            return chai.expect(client.searchAssets(filter)).to.eventually.to.be.an('array').that.is.not.empty
        })
    })

    describe('when calling the createFinding', function () {
        testIf('should return created finding', function () {
            // client
            let client = new Client(ACCOUNT_KEY_FILE, ORGANIZATION_ID, API_KEY)

            // params
            let sourceId = '9264282320683959279'
            let findingId = uuid4().replace(/-/g, '')

            // body
            let body = {
                state: 'ACTIVE',
                category: 'GCS Bucket author:lbotelho@clsecteam.com resourceType:gcs_bucket methodName:storage.buckets.create ADD roles/storage.legacyBucketOwner, ADD roles/storage.legacyBucketOwner, ADD roles/storage.legacyBucketReader bucket_name:testbucketcreation, location:us, project_id:tmp-scc-logs-beta',
                resourceName: '//storage.googleapis.com/wsxdfrvgyhbun',
                eventTime: '2018-12-04T14:09:17Z',
                externalUri: 'https://console.cloud.google.com/logs/viewer?project=tmp-scc-logs-beta&minLogLevel=0&expandAll=true&interval=NO_LIMIT&expandAll=true&advancedFilter=insertId%3D%22xaz7a9e6ph8m%22%0A',
                sourceProperties: {
                    insertId: 'xaz7a9e6ph8m',
                    logName: 'projects/tmp-scc-logs-beta/logs/cloudaudit.googleapis.com%2Factivity',
                    protoPayload_type: 'type.googleapis.com/google.cloud.audit.AuditLog',
                    protoPayload_authenticationInfo_principalEmail: 'lbotelho@clsecteam.com',
                    protoPayload_authorizationInfo: '[{\'granted\':true,\'permission\':\'storage.buckets.delete\',\'resource\':\'projects/_/buckets/wsxdfrvgyhbun\',\'resourceAttributes\':{}},{\'granted\':true,\'permission\':\'storage.buckets.getIamPolicy\',\'resource\':\'projects/_/buckets/wsxdfrvgyhbun\',\'resourceAttributes\':{}}]',
                    protoPayload_methodName: 'storage.buckets.delete',
                    protoPayload_requestMetadata_callerIp: '200.186.51.74',
                    protoPayload_requestMetadata_callerSuppliedUserAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36,gzip(gfe)',
                    protoPayload_resourceLocation_currentLocations: '[\'us\']',
                    protoPayload_resourceName: 'projects/_/buckets/wsxdfrvgyhbun',
                    protoPayload_serviceName: 'storage.googleapis.com',
                    receiveTimestamp: '2018-12-04T14:09:17.568617133Z',
                    resource_labels_bucket_name: 'wsxdfrvgyhbun',
                    resource_labels_location: 'us',
                    resource_labels_project_id: 'tmp-scc-logs-beta',
                    resource_type: 'gcs_bucket',
                    severity: 'NOTICE',
                    timestamp: '2018-12-04T14:09:17.266Z'
                }
            }

            // assert
            return chai.expect(client.createFinding(
                sourceId,
                findingId,
                body.category,
                body.state,
                body.resourceName,
                body.externalUri,
                body.sourceProperties,
                body.securityMarks,
                body.eventTime)).to.eventually.to.include({ status: 200 })
        })
    })

    describe('when calling the patchFinding', function () {
        testIf('should return created finding.', function () {
            // client
            let client = new Client(ACCOUNT_KEY_FILE, ORGANIZATION_ID, API_KEY)

            // params
            let sourceId = '9264282320683959279'
            let findingId = 'qqqqqqqqqqqqqqqqq'

            // body
            let body = {
                state: 'ACTIVE',
                category: 'GCS Bucket author:dandradex@clsecteam.com resourceType:gcs_bucket methodName:storage.buckets.create ADD roles/storage.legacyBucketOwner, ADD roles/storage.legacyBucketOwner, ADD roles/storage.legacyBucketReader bucket_name:testbucketcreation, location:us, project_id:tmp-scc-logs-beta',
                resourceName: '//storage.googleapis.com/wsxdfrvgyhbun',
                eventTime: '2018-12-04T14:09:17Z',
                externalUri: 'https://console.cloud.google.com/logs/viewer?project=tmp-scc-logs-beta&minLogLevel=0&expandAll=true&interval=NO_LIMIT&expandAll=true&advancedFilter=insertId%3D%22xaz7a9e6ph8m%22%0A',
                sourceProperties: {
                    insertId: 'xaz7a9e6ph8m',
                    logName: 'projects/tmp-scc-logs-beta/logs/cloudaudit.googleapis.com%2Factivity',
                    protoPayload_type: 'type.googleapis.com/google.cloud.audit.AuditLog',
                    protoPayload_authenticationInfo_principalEmail: 'lbotelho@clsecteam.com',
                    protoPayload_authorizationInfo: '[{\'granted\':true,\'permission\':\'storage.buckets.delete\',\'resource\':\'projects/_/buckets/wsxdfrvgyhbun\',\'resourceAttributes\':{}},{\'granted\':true,\'permission\':\'storage.buckets.getIamPolicy\',\'resource\':\'projects/_/buckets/wsxdfrvgyhbun\',\'resourceAttributes\':{}}]',
                    protoPayload_methodName: 'storage.buckets.delete',
                    protoPayload_requestMetadata_callerIp: '200.186.51.74',
                    protoPayload_requestMetadata_callerSuppliedUserAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36,gzip(gfe)',
                    protoPayload_resourceLocation_currentLocations: '[\'us\']',
                    protoPayload_resourceName: 'projects/_/buckets/wsxdfrvgyhbun',
                    protoPayload_serviceName: 'storage.googleapis.com',
                    receiveTimestamp: '2018-12-04T14:09:17.568617133Z',
                    resource_labels_bucket_name: 'wsxdfrvgyhbun',
                    resource_labels_location: 'us',
                    resource_labels_project_id: 'tmp-scc-logs-beta',
                    resource_type: 'gcs_bucket',
                    severity: 'NOTICE',
                    timestamp: '2018-12-04T14:09:17.266Z'
                }
            }

            // assert
            return chai.expect(client.patchFinding(
                sourceId,
                findingId,
                body.category,
                body.state,
                body.resourceName,
                body.externalUri,
                body.sourceProperties,
                body.securityMarks,
                body.eventTime)).to.eventually.to.include({ status: 200 })
        })
    })
}, 0)

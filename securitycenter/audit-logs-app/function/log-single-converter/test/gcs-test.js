'use strict';

// Imports
const fs = require('fs');
const moment = require('moment');
const should = require('should');
const gcsExamples = require('./samples/gcs_examples');
const converter = require('../converter');

describe('GCS log entry Mapping', function () {
    context('When recieving a GCS log entry', function () {
        it('should process a GCS bucket creation message.', function () {
            const createBucket = gcsExamples.createBucket();
            let source_finding = converter.convertToFinding(createBucket, {});
            source_finding.resourceName.should.equal('//storage.googleapis.com/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5');
            source_finding.category.should.equal('GCS Bucket author:dandrade@ciandt.com resourceType:gcs_bucket methodName:storage.buckets.create ADD roles/storage.legacyBucketOwner projectOwner:noti-201808221442-a, ADD roles/storage.legacyBucketOwner projectEditor:noti-201808221442-a, ADD roles/storage.legacyBucketReader projectViewer:noti-201808221442-a bucket_name:n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5, location:US-CENTRAL1, project_id:noti-201808221442-a');
            source_finding.eventTime.should.equal('2018-09-05T19:40:26Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('storage.buckets.create');
            source_finding.sourceProperties.resource_type.should.equal('gcs_bucket');
        });
        it('should process a GCS bucket deletion message.', function () {
            const deleteBucket = gcsExamples.deleteBucket();
            let source_finding = converter.convertToFinding(deleteBucket, {});
            source_finding.resourceName.should.equal('//storage.googleapis.com/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5');
            source_finding.category.should.equal('GCS Bucket author:dandrade@ciandt.com resourceType:gcs_bucket methodName:storage.buckets.delete bucket_name:n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5, location:US-CENTRAL1, project_id:noti-201808221442-a');
            source_finding.eventTime.should.equal('2018-09-05T19:45:16Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('storage.buckets.delete');
            source_finding.sourceProperties.resource_type.should.equal('gcs_bucket');
        });
        it('should process a GCS bucket set I am Permissions message.', function () {
            const setIamPermissions = gcsExamples.setIamPermissions();
            let source_finding = converter.convertToFinding(setIamPermissions, {});
            source_finding.resourceName.should.equal('//storage.googleapis.com/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5');
            source_finding.category.should.equal('GCS Bucket author:dandrade@ciandt.com resourceType:gcs_bucket methodName:storage.setIamPermissions ADD roles/storage.objectViewer user:dandrade@ciandt.com bucket_name:n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5, location:US-CENTRAL1, project_id:noti-201808221442-a');
            source_finding.eventTime.should.equal('2018-09-05T19:41:08Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('storage.setIamPermissions');
            source_finding.sourceProperties.resource_type.should.equal('gcs_bucket');
        });
        it('should process a GCS bucket object update message.', function () {
            const updateBucket = gcsExamples.updateBucket();
            let source_finding = converter.convertToFinding(updateBucket, {});
            source_finding.resourceName.should.equal('//storage.googleapis.com/n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5/objects/set_iam_policy.json');
            source_finding.category.should.equal('GCS Bucket author:dandrade@ciandt.com resourceType:gcs_bucket methodName:storage.objects.update REMOVE roles/storage.legacyObjectReader projectEditor:noti-201808221442-a, ADD roles/storage.legacyObjectOwner projectEditor:noti-201808221442-a bucket_name:n45g9jh45g9j45g9j46g9j46g9j5369j639j8659j8t3h5, location:US-CENTRAL1, project_id:noti-201808221442-a');
            source_finding.eventTime.should.equal('2018-09-05T19:44:56Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.externalUri.should.equal('https://console.cloud.google.com/logs/viewer?project=noti-201808221442-a&minLogLevel=0&expandAll=true&interval=NO_LIMIT&expandAll=true&advancedFilter=insertId%3D%22-wqn6mteg5upq%22%0A');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('storage.objects.update');
            source_finding.sourceProperties.resource_type.should.equal('gcs_bucket');
        });
    });
});
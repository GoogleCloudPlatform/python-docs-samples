'use-strict'

//Imports
const should = require('should');
const jsonMocks = require('./samples/generic_examples');
const converter = require('../converter');

describe('Generic unmapped log entry', function () {
    context('When recieving an Big Query insert log entry', function () {
        it('should process an finding with Big Query insert categorized', function () {
            const createBigQueryJson = jsonMocks.createBigQueryJson();
            let sourceFinding = converter.convertToFinding(createBigQueryJson, {});
            sourceFinding.category.should.equal('BigQuery author:tribeiro@clsecteam.com resourceType:bigquery_resource methodName:datasetservice.insert project_id:gce-logging-audit');
            sourceFinding.resourceName.should.equal('//bigquery.googleapis.com/projects/gce-logging-audit/datasets');
            sourceFinding.eventTime.should.equal('2018-09-12T18:55:36Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/gce-logging-audit/datasets');
        });
        it('should process an finding with Spanner Instance insert categorized', function () {
            const createSpannerJson = jsonMocks.createSpannerJson();
            let sourceFinding = converter.convertToFinding(createSpannerJson, {});
            sourceFinding.category.should.equal('Cloud Spanner Instance author:tribeiro@clsecteam.com resourceType:spanner_instance methodName:google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance instance_config:, instance_id:test-spanner, location:, project_id:gce-logging-audit');
            sourceFinding.resourceName.should.equal('//spanner.googleapis.com/projects/gce-logging-audit/instances/test-spanner');
            sourceFinding.eventTime.should.equal('2018-09-12T18:41:24Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/gce-logging-audit/instances/test-spanner');
        });
    });
});
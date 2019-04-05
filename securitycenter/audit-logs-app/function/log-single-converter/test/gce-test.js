'use strict';

// Imports
const fs = require('fs');
const moment = require('moment');
const should = require('should');
const GceSamples = require('./samples/gce_samples');
const converter = require('../converter');

function publish(finding) {return Promise.resolve(finding.resourceName)}

describe('GCE log entry Mapping', function () {
    context('When recieving a GCE log entry', function () {
        it('should process a GCE create Instance message.', function () {
            const createInstance = GceSamples.createInstance();
            let source_finding = converter.convertToFinding(createInstance, {});
            source_finding.resourceName.should.equal('//compute.googleapis.com/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1');
            source_finding.category.should.equal('GCE VM Instance author:dandrade@ciandt.com resourceType:gce_instance methodName:beta.compute.instances.insert instance_id:7001864148707138537, project_id:gce-audit-logs-216020, zone:us-east1-b');
            source_finding.eventTime.should.equal('2018-09-10T21:41:26Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('beta.compute.instances.insert');
            source_finding.sourceProperties.resource_type.should.equal('gce_instance');
        });
        it('should process a GCE delete Instance message.', function () {
            const deleteInstance = GceSamples.deleteInstance();
            let source_finding = converter.convertToFinding(deleteInstance, {});
            source_finding.resourceName.should.equal('//compute.googleapis.com/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1');
            source_finding.category.should.equal('GCE VM Instance author:dandrade@ciandt.com resourceType:gce_instance methodName:v1.compute.instances.delete instance_id:7001864148707138537, project_id:gce-audit-logs-216020, zone:us-east1-b');
            source_finding.eventTime.should.equal('2018-09-10T22:53:29Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('v1.compute.instances.delete');
            source_finding.sourceProperties.resource_type.should.equal('gce_instance');
        });
        it('should process a GCE set Tags message.', function () {
            const setTags = GceSamples.setTags();
            let source_finding = converter.convertToFinding(setTags, {});
            source_finding.resourceName.should.equal('//compute.googleapis.com/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1');
            source_finding.category.should.equal('GCE VM Instance author:dandrade@ciandt.com resourceType:gce_instance methodName:v1.compute.instances.setTags instance_id:7001864148707138537, project_id:gce-audit-logs-216020, zone:us-east1-b');
            source_finding.eventTime.should.equal('2018-09-10T21:43:39Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('v1.compute.instances.setTags');
            source_finding.sourceProperties.resource_type.should.equal('gce_instance');
        });
        xit('should process a GCE set Common Instance Metadata message.', () => {
            const setCommonInstanceMetadata = GceSamples.setCommonInstanceMetadata();
            return converter.convertWithExtraInfo(setCommonInstanceMetadata, publish).should.be.eventually.equal('//cloudresourcemanager.googleapis.com/projects/620146303431');
        }).timeout(60000);
        xit('should process a DNS Zone deletion.', () => {
            const deleteDnsZone = GceSamples.deleteDnsZone();
            return converter.convertWithExtraInfo(deleteDnsZone, publish).should.be.eventually.equal('//dns.googleapis.com/projects/759835331192/managedZones/demo-zone');
        }).timeout(60000);
    });
});
'use-strict'

//Imports
const fs = require('fs');
const moment = require('moment');
const should = require('should');
const jsonMocks = require('./samples/networkSamples');
const converter = require('../converter');

describe('Network log entry Mapping', function () {
    context('When recieving an network log entry', function () {
        it('should process an CREATE network message  ', function () {
            const createNetworkJson = jsonMocks.createNetworkJson();
            let sourceFinding = converter.convertToFinding(createNetworkJson, {});
            sourceFinding.category.should.equal('GCE Network author:lucasbr@clsecteam.com resourceType:gce_network methodName:v1.compute.networks.insert network_id:7505145839472187905, project_id:scc-log-pubsub');
            sourceFinding.resourceName.should.equal('//compute.googleapis.com/projects/scc-log-pubsub/global/networks/scc-log-network');
            sourceFinding.eventTime.should.equal('2018-09-05T18:48:12Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/scc-log-pubsub/global/networks/scc-log-network');
        });
        it('should process an DELETE network message', function () {
            const deleteNetworkJson = jsonMocks.deleteNetworkJson();
            let sourceFinding = converter.convertToFinding(deleteNetworkJson, {});
            sourceFinding.category.should.equal('GCE Network author:lucasbr@clsecteam.com resourceType:gce_network methodName:v1.compute.networks.delete network_id:7505145839472187905, project_id:scc-log-pubsub');
            sourceFinding.resourceName.should.equal('//compute.googleapis.com/projects/scc-log-pubsub/global/networks/scc-log-network');
            sourceFinding.eventTime.should.equal('2018-09-05T19:21:23Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/scc-log-pubsub/global/networks/scc-log-network');
        });
        it('should process an CREATE subnetwork message', function () {
            const createSubnetworkJson = jsonMocks.createSubnetworkJson();
            let sourceFinding = converter.convertToFinding(createSubnetworkJson, {});
            sourceFinding.category.should.equal('GCE Subnetwork author:lucasbr@clsecteam.com resourceType:gce_subnetwork methodName:v1.compute.subnetworks.insert location:us-central1, project_id:scc-log-pubsub, subnetwork_id:6718876411500464984, subnetwork_name:scc-subnetwork-01');
            sourceFinding.resourceName.should.equal('//compute.googleapis.com/projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01');
            sourceFinding.eventTime.should.equal('2018-09-06T14:12:06Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01');
        });
        it('should process an DELETE subnetwork message', function () {
            const deleteSubnetworkJson = jsonMocks.deleteSubnetworkJson();
            let sourceFinding = converter.convertToFinding(deleteSubnetworkJson, {});
            sourceFinding.category.should.equal('GCE Subnetwork author:lucasbr@clsecteam.com resourceType:gce_subnetwork methodName:beta.compute.subnetworks.delete location:us-central1, project_id:scc-log-pubsub, subnetwork_id:6718876411500464984, subnetwork_name:scc-subnetwork-01');
            sourceFinding.resourceName.should.equal('//compute.googleapis.com/projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01');
            sourceFinding.eventTime.should.equal('2018-09-06T14:37:13Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/scc-log-pubsub/regions/us-central1/subnetworks/scc-subnetwork-01');
        });
        it('should process an CREATE firewall message', function () {
            const createFirewallJson = jsonMocks.createFirewallJson();
            let sourceFinding = converter.convertToFinding(createFirewallJson, {});
            sourceFinding.category.should.equal('GCE Firewall Rule author:lucasbr@clsecteam.com resourceType:gce_firewall_rule methodName:v1.compute.firewalls.insert firewall_rule_id:5133249119463966455, project_id:scc-log-pubsub');
            sourceFinding.resourceName.should.equal('//compute.googleapis.com/projects/scc-log-pubsub/global/firewalls/firewall-rule-01');
            sourceFinding.eventTime.should.equal('2018-09-06T14:22:15Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/scc-log-pubsub/global/firewalls/firewall-rule-01');
        });
        it('should process an DELETE firewall message', function () {
            const deleteFirewallJson = jsonMocks.deleteFirewallJson();
            let sourceFinding = converter.convertToFinding(deleteFirewallJson, {});
            sourceFinding.category.should.equal('GCE Firewall Rule author:lucasbr@clsecteam.com resourceType:gce_firewall_rule methodName:v1.compute.firewalls.delete firewall_rule_id:5133249119463966455, project_id:scc-log-pubsub');
            sourceFinding.resourceName.should.equal('//compute.googleapis.com/projects/scc-log-pubsub/global/firewalls/firewall-rule-01');
            sourceFinding.eventTime.should.equal('2018-09-06T14:29:03Z');
            sourceFinding.sourceProperties.severity.should.equal('NOTICE');
            sourceFinding.sourceProperties.protoPayload_resourceName.should.equal('projects/scc-log-pubsub/global/firewalls/firewall-rule-01');
        })
    });
});
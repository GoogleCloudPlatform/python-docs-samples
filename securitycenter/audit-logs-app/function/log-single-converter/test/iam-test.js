'use strict';

// Imports
const fs = require('fs');
const moment = require('moment');
const should = require('should');
const json_examples = require('./samples/json_examples');
const converter = require('../converter');

const set_iam_policy_json = json_examples.set_iam_policy_json();

describe('IAM log entry Mapping', function () {
    context('When recieving an IAM log entry', function () {
        it('should process an ADD setIamPolicy message for Organization', function () {
            let source_finding = converter.convertToFinding(set_iam_policy_json, {});
            source_finding.category.should.equal('SetIamPolicy author:johndoe@example.com resourceType:organization methodName:SetIamPolicy ADD roles/compute.securityAdmin serviceAccount:forseti@example.iam.gserviceaccount.com organization_id:0000000000000');
            source_finding.resourceName.should.equal('//cloudresourcemanager.googleapis.com/organizations/0000000000000');
            source_finding.eventTime.should.equal('2018-09-04T17:49:04Z');
            source_finding.sourceProperties.severity.should.equal('NOTICE');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('SetIamPolicy');
        })
    });
});
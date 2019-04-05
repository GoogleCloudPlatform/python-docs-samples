'use strict';

// Imports
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');
const cleaner = require('../index');
const findingsParser = require('../findings-parser')
const fs = require('fs');
const yaml = require('js-yaml');
const moment = require('moment');

// Constants
const expect = chai.expect;

// Pre setup
chai.use(chaiAsPromised);

const MESSAGE = {
  data: {
    data: 'The message'
  }
}

describe('Cleanup', function () {

    describe('#handle()', function () {

      describe('findings parser', function () {
          context('when it have a valid JSON file', function () {
              it('should return a Array[Object]', function () {
                const originalValue = [{
                  "marks": {},
                  "id": "1062898918192-/cloud/project_id/white-list-195009/policy_violation/COIN_MINING",
                  "assetId": "white-list-195009/instance/1212099906983003493",
                  "scannerId": "GOOGLE_ANOMALY_DETECTION",
                  "updateTime": {
                    "seconds": "1521237200",
                    "nanos": 966000000
                  },
                  "properties": {
                    "fields": {
                      "action": {
                        "stringValue": "RESTRICT_RESOURCES",
                        "kind": "stringValue"
                      },
                      "scc_source_category_id": {
                        "stringValue": "COIN_MINING",
                        "kind": "stringValue"
                      },
                      "scc_status": {
                        "stringValue": "ACTIVE",
                        "kind": "stringValue"
                      },
                      "product": {
                        "stringValue": "compute_engine",
                        "kind": "stringValue"
                      },
                      "url": {
                        "stringValue": "",
                        "kind": "stringValue"
                      }
                    }
                  }
                }]
                const expected = [{
                  id: "1062898918192-/cloud/project_id/white-list-195009/policy_violation/COIN_MINING",
                  sourceId: "GOOGLE_ANOMALY_DETECTION",
                  assetIds: [ "white-list-195009/instance/1212099906983003493" ],
                  category: "COIN_MINING",
                  url: "",
                  eventTime: {
                      seconds: "1521237201",
                      nanos: 966000000
                  },
                  properties: {
                    fields: {
                      action: {
                        stringValue: "RESTRICT_RESOURCES"
                      },
                      scc_source_category_id: {
                        stringValue: "COIN_MINING"
                      },
                      scc_status: {
                        stringValue: "INACTIVE"
                      },
                      product: {
                        stringValue: "compute_engine"
                      }
                    }
                  }
                }]
                let executed = findingsParser.parseToDeletedSourceFindings(originalValue);
                return expect(executed).to.be.eql(expected);
              });
          });
      });

      describe('executing cleanup', function () {
        context('when it have a valid findings', function () {
            it('should pass', function () {
              cleaner.cleanUp(MESSAGE);
            });
        });
      });

    });

});
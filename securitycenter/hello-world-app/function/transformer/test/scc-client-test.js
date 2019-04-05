'use strict';

// Imports
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');
const { Client } = require('../scc-client');
const fs = require('fs');

// Constants
const expect = chai.expect;
const ACCOUNT_KEY_FILE = __dirname + '/../accounts/cscc_api_client.json';
const ORGANIZATION_ID = '0000000000000'; // Change to real org id
const API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'; // Change to real api key

// Pre setup
chai.use(chaiAsPromised);

describe('SCC Rest Client', function () {
    context('When calling the searchAssets', function () {
        it('should return all assets from organization using filter.', function () {
            if (fs.existsSync(ACCOUNT_KEY_FILE)) {
                // given
                this.timeout(0);
                const client = new Client(ACCOUNT_KEY_FILE, ORGANIZATION_ID, API_KEY);
                const filter = 'security_center_properties.resource_type : "Project"';
                // when
                return expect(client.searchAssets(filter))
                    // then
                    .to.eventually.to.be.an('array').that.is.not.empty;
            } else {
                this.skip();
            }
        })
    })
});

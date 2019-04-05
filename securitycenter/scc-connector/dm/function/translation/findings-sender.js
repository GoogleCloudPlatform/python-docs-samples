'use strict';

// Imports
const securitycenterModule = require('securitycenter/src/v1alpha3');
const async = require('async')
const config = require("./config.json");

// Constants
const ACCOUNT_KEY_FILE = __dirname + '/accounts/cscc_api_client.json';
// Set this to zero to ignore a SCC request wait time
const RESPONSE_WAIT_TIME = config.SCC_REQUEST_THROTTLING_WAIT_TIME

/**
 * Call the CSCC API to send the findings mapped from partners.
 * 
 * @param {!Array<Object>} findings The findings to be send to CSCC.
 * @param {!String} orgName The organization name.
 * @param {!String} servicePath The service path from CSCC API.
 * @param {!String} serviceAccountPath The service account path from CSCC API.
 * @returns Returns a Promise.
 */
function sendWithServiceAccount(findings, orgName, servicePath, serviceAccountPath) {
    const client = new securitycenterModule.SecurityCenterClient({
        keyFilename: serviceAccountPath,
        servicePath: servicePath || securitycenterModule.SecurityCenterClient.servicePath
    })
    
    // Call CSCC API
    async.eachSeries(findings, 
        (finding, cb) => {
            return client.createFinding({
                orgName: orgName,
                sourceFinding: finding
            }).then(res => {
                console.log(JSON.stringify(res));
                if (RESPONSE_WAIT_TIME) {
                    setTimeout(() => {
                        cb(null);
                    }, RESPONSE_WAIT_TIME);
                }
            }).catch(err => {
                console.error(err);
                cb(err);
            });
        },
        (err) => {
            console.error(err)
        }
    );
}

/**
 * Call the CSCC API to send the findings mapped from partners.
 * 
 * @param {!Array<Object>} findings The findings to be send to CSCC.
 * @param {!String} orgName The organization name.
 * @param {!String} servicePath The service path from CSCC API.
 * @returns Returns a Promise.
 */
function send(findings, orgName, servicePath) {    
    return sendWithServiceAccount(findings, orgName, servicePath, ACCOUNT_KEY_FILE);
}

module.exports.send = send;
module.exports.sendWithServiceAccount = sendWithServiceAccount;

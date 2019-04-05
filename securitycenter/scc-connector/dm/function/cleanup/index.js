'use strict';

// Imports
const PubSub = require('@google-cloud/pubsub');
const csccService = require('./cscc-service');
const findingsParser = require('./findings-parser');

// Constants that must to be overrided on build to get orgName and servicePath
const orgName = null, servicePath = null;

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.cleanUp = (event) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64');
    console.log(`Receiving message: ${strMessage}`);

    return Promise.resolve()
    .then(() => {
        //Get finding from cscc
        return csccService.getCsccFindings(orgName, servicePath);
    })
    .then((foundFindings) => {
        //Parse findings to source_findings
        return findingsParser.parseToDeletedSourceFindings(foundFindings);
    })
    .then((sourceFindings) => {
        //Submit to cscc the updated findings as deleted
        return csccService.upsertFindings(sourceFindings, orgName, servicePath);
    })
    .then((response) => {
        if (response) {
            let errorsReason = []
            let failed = response.filter(item => {
                if (item.message) {
                    if (errorsReason.indexOf(item.message) === -1) {
                        errorsReason.push(item.message);
                    }
                    return item;
                }
            });
            console.log('Number of findings processed: ', response.length);
            if (failed.length) {
                console.log('Number of findings failed to update: ', failed.length);
                console.log('Errors reason:', errorsReason.join(' - '));
            }
            console.log('Number of findings updated successfully: ', response.length - failed.length);
        }
    });

};

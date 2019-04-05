'use strict';

// Imports
const PubSub = require('@google-cloud/pubsub');
const { Client } = require('./scc-client')

// Constants
const TOPIC_NAME = 'redirect';
const ACCOUNT_KEY_FILE = __dirname + '/accounts/cscc_api_client.json';
const { ORG_ID, API_KEY } = require("./config.json");
const FILTER = 'security_center_properties.resource_type : "Project"';

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.transform = (event) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64').toString();
    console.log(`Receiving message: ${strMessage}`);

    const client = new Client(ACCOUNT_KEY_FILE, ORG_ID, API_KEY);

    // Finding assets on scc
    return client.searchAssets(FILTER)
        .then(resources => {
            const assetsNames = [];
            // Get only asset name to send to topic
            for (let i = 0; i < resources.length; i++) {
                assetsNames.push(resources[i].asset.name);
            }

            // Publishes file data to topic
            const dataJSON = Buffer.from(`{
                "Assets names found on organization ${ORG_ID} using filter ${FILTER}": "${assetsNames}"
            }`);

            return new PubSub()
                .topic(TOPIC_NAME)
                .publisher()
                .publish(dataJSON)
                .then(() => {
                    console.log('Message published.');
                });
        })
        .catch(err => {
            console.error('ERROR:', err);
        });
};

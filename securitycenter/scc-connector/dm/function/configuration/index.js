'use strict';

// Imports
const Datastore = require('@google-cloud/datastore');

// Constants
const namespace = 'findings';
const dataStoreConfigKind = 'Configuration';
const dataStoreConfigEntityName = 'writer';

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.saveConfiguration = (event) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64');
    console.log(`Receiving message: ${strMessage}`);
    const pubsubMessage = JSON.parse(strMessage);

    // Configs
    const mode = pubsubMessage.mode;

    // Persists configuration
    const datastore = new Datastore();
    const dsKey = datastore.key({
        namespace: namespace,
        path: [dataStoreConfigKind, dataStoreConfigEntityName]
    });
    const entity = {
        key: dsKey,
        data: {
            mode: mode
        }
    };
    
    console.log(`Persisting entity: ${JSON.stringify(entity)}`);
    
    return datastore.save(entity);
};

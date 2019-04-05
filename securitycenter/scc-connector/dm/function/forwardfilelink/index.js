'use strict';

// Imports
const Datastore = require('@google-cloud/datastore');
const PubSub = require('@google-cloud/pubsub');

// Constants
const namespace = 'findings';
const dataStoreConfigKind = 'Configuration';
const dataStoreConfigEntityName = 'writer';
const dataStoreBucketFileKind = 'Buffer';
const dataStoreBucketFileEntityName = 'writer';
const translationTopicName = 'translation';

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.subscribeFindings = (event) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64');
    console.log(`Receiving message: ${strMessage}`);
    const pubsubMessage = JSON.parse(strMessage);

    // Configs
    const bucketName = pubsubMessage.bucket;
    const srcFilename = pubsubMessage.name;

    // Reads configurations from DataStore.
    const datastore = new Datastore();
    const dsKey = datastore.key({
        namespace: namespace,
        path: [dataStoreConfigKind, dataStoreConfigEntityName]
    });
    console.log(`Get configuration using key: ${JSON.stringify(dsKey)}`);
    return datastore
        .get(dsKey)
        .then(entities => {
            // Config entity
            let mode = 'prod';
            if (entities[0] && entities[0].mode) {
                mode = entities[0].mode;
                console.log(`Configuration mode: ${mode}`);
            } else {
                console.log(`No configuration found using default mode: ${mode}`);
            }

            if (mode === 'prod') {
                // Publishes file data to prod mode on translation topic
                const dataJSON = Buffer.from(`{
                    "bucketName": "${bucketName}",
                    "filename": "${srcFilename}"
                }`);
                const pubsub = new PubSub();
                return pubsub
                    .topic(translationTopicName)
                    .publisher()
                    .publish(dataJSON)
                    .then(results => {
                        console.log(`Message ${dataJSON} published.`);
                    });
            } else {
                // Persists file data to demo mode
                const dsKey = datastore.key({
                    namespace: namespace,
                    path: [dataStoreBucketFileKind, dataStoreBucketFileEntityName]
                });
                const entity = {
                    key: dsKey,
                    data: {
                        bucketName: bucketName,
                        filename: srcFilename
                    }
                };
                console.log(`Persisting entity: ${JSON.stringify(entity)}`);
                return datastore.save(entity);
            }
        });
};

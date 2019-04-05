'use strict';

// Imports
const PubSub = require('@google-cloud/pubsub');
const Datastore = require('@google-cloud/datastore');

// Constants
const namespace = 'findings';
const dataStoreBucketFileKind = 'Buffer';
const dataStoreBucketFileEntityName = 'writer';
const translationTopicName = 'translation';

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.flushBuffer = (event) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64');
    console.log(`Receiving message: ${strMessage}`);

    // Reads file data from DataStore.
    const datastore = new Datastore();
    const dsKey = datastore.key({
        namespace: namespace,
        path: [dataStoreBucketFileKind, dataStoreBucketFileEntityName]
    });
    console.log(`Get file data using key: ${JSON.stringify(dsKey)}`);
    return datastore
        .get(dsKey)
        .then(entities => {
            const entity = entities[0];
            if (entity && entity.bucketName && entity.filename) {

                // Publishes file data to translation topic
                const dataJSON = Buffer.from(`{
                    "bucketName": "${entity.bucketName}",
                    "filename": "${entity.filename}"
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
                console.error('ERROR: No file data found');
            }
        });
};

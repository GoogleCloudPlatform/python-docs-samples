'use strict';

// Imports
const converter = require('./converter');
const PubSub = require('@google-cloud/pubsub');

// Constants
const TOPIC_NAME = 'topic_single_findings';
const pubsubclient = new PubSub()
const topicSingleFindings = pubsubclient.topic(TOPIC_NAME)



function publishFinding(finding) {
    if (finding) {
        const srtFinding = JSON.stringify(finding);
        console.log(`Finding json: ${srtFinding}`);
    
        return topicSingleFindings
            .publisher()
            .publish(Buffer.from(srtFinding))
            .then(results => {
                console.log('Message published.');
            });
    }
}

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.convert = (event) => {
    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64').toString();
    console.log(`Receiving message: ${strMessage}`);
    const logItem = JSON.parse(strMessage);
    return converter.convertWithExtraInfo(logItem, publishFinding);
   
};

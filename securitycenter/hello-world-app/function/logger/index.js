'use strict';

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 * @param {!function } callback The callback function.
 */
exports.log = (event, callback) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64');
    console.log(`Receiving message: ${strMessage}`);

    callback();
};

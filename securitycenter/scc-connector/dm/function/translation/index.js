'use strict';

// Imports
const fs = require('fs');
const os = require('os');
const path = require('path');
const Storage = require('@google-cloud/storage');
const yaml = require('js-yaml');
const jsonHandler = require('./json-handler');
const csvHandler = require('./csv-handler');
const sender = require('./findings-sender');

// Constants
const localFileName = 'findings.json';

/**
 * Parse downloaded file.
 * 
 * @param {!String} filePath The local file path.
 * @returns Returns a Promise.
 */
function parseFile(filePath) {

    // Get content from file
    const contents = fs.createReadStream(filePath);
    const mapper = yaml.safeLoad(fs.readFileSync('./mapper.yaml', 'utf8'));

    // Log mapper content
    console.log(`Mapper content: ${JSON.stringify(mapper)}`)

    let handler = null;
    switch (mapper.type) {
        case 'csv':
            handler = csvHandler;
            break;
        case 'json':
            handler = jsonHandler;
            break;
        default:
            return Promise.reject(`ERROR: Mapper type unknown = ${mapper.type}`);
    }

    return handler.handle(contents, mapper)
        .then(findings => {
            return sender.send(findings, mapper.org_name, mapper.service_path);
        });
}

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 */
exports.translate = (event) => {

    // The Cloud Pub/Sub Message object.
    const encodedMessage = event.data.data;
    const strMessage = Buffer.from(encodedMessage, 'base64');
    console.log(`Receiving message: ${strMessage}`);
    const pubsubMessage = JSON.parse(strMessage);

    // Configs
    const bucketName = pubsubMessage.bucketName;
    const srcFilename = pubsubMessage.filename;
    const destFilename = path.join(os.tmpdir(), localFileName);

    // Creates a client
    const storage = new Storage();
    const options = {
        // The path to which the file should be downloaded, e.g. "./file.txt"
        destination: destFilename
    };

    // Downloads the file
    return storage
        .bucket(bucketName)
        .file(srcFilename)
        .download(options)
        .then(() => {
            console.log(
                `gs://${bucketName}/${srcFilename} downloaded to ${destFilename}.`
            );
            return parseFile(destFilename);
        })
        .catch(err => {
            console.error('ERROR:', err);
        });
};

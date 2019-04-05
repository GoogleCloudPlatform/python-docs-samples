'use strict'

const uuid4 = require('uuid4')
const { Client } = require('scc-client')

// create scc client
const ACCOUNT_KEY_FILE = __dirname + '/accounts/cscc_api_client.json'
const client = new Client(ACCOUNT_KEY_FILE, process.env.ORGANIZATION_ID, process.env.API_KEY)

function generateFindingId(finding) {
    if (finding.hasOwnProperty('id')) {
        let findingId = finding.id;
        delete finding.id;
        return findingId;
    }
    return uuid4().replace(/-/g, '');
};

function selectSourceId(finding) {
    if (finding['sourceProperties'].hasOwnProperty('binaryAuthorization') && finding['sourceProperties']['binaryAuthorization'] === 'true') {
        delete finding.sourceProperties.binaryAuthorization
        return process.env.BIN_AUTH_SOURCE_ID;
    }
    return process.env.SOURCE_ID;
};

/**
* Triggered from a message on a Cloud Pub/Sub topic.
*
* @param {!Object} event Event payload and metadata.
* @param {!Function} callback Callback function to signal completion.
*/
exports.sendFinding = (event, callback) => {
    // get pubsub message
    let pubsubMessage = event.data
    
    // get finding from message
    let finding = JSON.parse(Buffer.from(pubsubMessage.data, 'base64').toString())
    console.log('received message: ' + JSON.stringify(finding))

    // params
    let sourceId = selectSourceId(finding)
    let findingId = generateFindingId(finding)

    // create finding
    return client.patchFinding(
        sourceId,
        findingId,
        finding.category,
        finding.state,
        finding.resourceName,
        finding.externalUri,
        finding.sourceProperties,
        finding.securityMarks,
        finding.eventTime)
        .then(res => {
            console.log('success creating finding: ', res)
            callback()
        }).catch(err => {
            console.error('error creating finding: ', err)
            callback()
        })
}

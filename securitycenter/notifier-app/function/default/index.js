"use strict";

const config = require("./config.json");

const SECURITY_HEADER = "x-client-key";

function verifyWebhook(request) {
    var token = request.get(SECURITY_HEADER);
    if ((token === undefined || token === null) || token !== config.CLIENT_KEY) {
        const error = new Error("Unauthorized");
        error.code = 401;
        throw error;
    }
}

/**
 * Cloud Function.
 *
 * @param {object} The http request object.
 * @param {object} The http response object.
 */
exports[config.APPLICATION_VERSION + "_notifyDefaultHttp"] = function notifyDefaultHttp(req, res) {
    try {
        verifyWebhook(req);
        var reqBody = JSON.stringify(req.body);
        console.log(`Request Body: ${reqBody}`);
        res.send(`Notification accepted.`);

    } catch (err) {
        console.error(err);
        res.status(err.code || 500).send(err);
    }

};
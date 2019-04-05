'use strict'

// imports
const moment = require('moment')
const ellipsis = require('text-ellipsis')
const { google } = require('googleapis')

// constants
const SCOPES = 'https://www.googleapis.com/auth/cloud-platform'
const DISCOVERY_URL = 'https://securitycenter.googleapis.com/$discovery/rest?key='
const PAGE_SIZE = 100

const MAX_CATEGORY_SIZE = 255

class Client {
    constructor(keyFilename, orgID, apiKey) {
        this.organizationId = orgID
        this.auth = google.auth.fromJSON(require(keyFilename))
        this.auth.scopes = SCOPES
        this.discoveryEndpoint = DISCOVERY_URL + apiKey
    }

    _patchFinding(sourceId, findingId, finding) {
        let req = {
            name: `organizations/${this.organizationId}/sources/${sourceId}/findings/${findingId}`,
            requestBody: finding
        }
        return google.discoverAPI(this.discoveryEndpoint, { auth: this.auth})
            .then(api => {
                return api.organizations.sources.findings.patch(req);
            })
    }

    patchFinding(sourceId, findingId, category, state, resourceName, externalUri, sourceProperties, securityMarks, eventTime) {
        let finding = {
            category: ellipsis(category || '', MAX_CATEGORY_SIZE),
            eventTime: eventTime || moment().utc().format(),
            externalUri: externalUri,
            resourceName: resourceName,
            securityMarks: securityMarks || {},
            sourceProperties: sourceProperties || {},
            state: state
        }
        return this._patchFinding(sourceId, findingId, finding)
    }

    _createFinding(sourceId, findingId, finding) {
        let req = {
            parent: `organizations/${this.organizationId}/sources/${sourceId}`,
            findingId: findingId,
            requestBody: finding
        }

        return google.discoverAPI(this.discoveryEndpoint, { auth: this.auth })
            .then(api => {
                return api.organizations.sources.findings.create(req)
            })
    }

    createFinding(sourceId, findingId, category, state, resourceName, externalUri, sourceProperties, securityMarks, eventTime) {
        let finding = {
            category: ellipsis(category || '', MAX_CATEGORY_SIZE),
            eventTime: eventTime || moment().utc().format(),
            externalUri: externalUri,
            resourceName: resourceName,
            securityMarks: securityMarks || {},
            sourceProperties: sourceProperties || {},
            state: state
        }
        return this._createFinding(sourceId, findingId, finding)
    }

    _paginatedSearch(api, prevResults, _filter, nextPageToken) {
        if (prevResults && prevResults.length && !nextPageToken) {
            return prevResults
        } else {
            return api.organizations.assets
                .list({
                    parent: `organizations/${this.organizationId}`,
                    filter: _filter,
                    page_token: nextPageToken,
                    page_size: PAGE_SIZE
                })
                .then(resp => {
                    const results = resp.data.listAssetsResults
                    if (results) {
                        prevResults.push(...results)
                        nextPageToken = resp.data.nextPageToken
                        return this._paginatedSearch(api, prevResults, _filter, nextPageToken)
                    } else {
                        return prevResults
                    }
                })
        }
    }

    searchAssets(_filter) {
        return google.discoverAPI(this.discoveryEndpoint, { auth: this.auth })
            .then(api => {
                return this._paginatedSearch(api, [], _filter, null)
            })
    }
}

exports.Client = Client

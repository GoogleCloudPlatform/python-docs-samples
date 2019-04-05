'use strict';

// Imports
const { google } = require('googleapis');

// Constants
const SCOPES = 'https://www.googleapis.com/auth/cloud-platform';
const DISCOVERY_URL = 'https://securitycenter.googleapis.com/$discovery/rest?key=';
const PAGE_SIZE = 100;

class Client {
    constructor(keyFilename, orgID, apiKey) {
        this.parent = `organizations/${orgID}`;
        this.auth = google.auth.fromJSON(require(keyFilename));
        this.auth.scopes = SCOPES;
        this.discoveryEndpoint = DISCOVERY_URL + apiKey;
    }

    _paginatedSearch(api, prevResults, _filter, nextPageToken) {
        if (prevResults && prevResults.length && !nextPageToken) {
            return prevResults;
        } else {
            return api.organizations.assets
                .list({
                    parent: this.parent,
                    filter: _filter,
                    page_token: nextPageToken,
                    page_size: PAGE_SIZE
                })
                .then(resp => {
                    const results = resp.data.listAssetsResults;
                    if (results) {
                        prevResults.push(...results);
                        nextPageToken = resp.data.nextPageToken;
                        return this._paginatedSearch(api, prevResults, _filter, nextPageToken);
                    } else {
                        return prevResults;
                    }
                });
        }
    }

    searchAssets(_filter) {
        return google.discoverAPI(this.discoveryEndpoint, { auth: this.auth })
            .then(api => {
                return this._paginatedSearch(api, [], _filter, null);
            })
    }
}

exports.Client = Client;

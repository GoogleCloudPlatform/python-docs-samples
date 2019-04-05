'use strict';

// Imports
const securitycenterModule = require('securitycenter/src/v1alpha3');

// Constants
const ACCOUNT_KEY_FILE = __dirname + '/accounts/cscc_api_client.json';

// Generate a the client CSCC API to be called
function generateClient(servicePath) {
  const client = new securitycenterModule.SecurityCenterClient({
      keyFilename: ACCOUNT_KEY_FILE,
      servicePath: servicePath
  });

  return client;
}

// Get all ACTIVE cscc findings for a organization
exports.getCsccFindings = (orgName, servicePath) => {
  // getting default values to run unit tests
  servicePath = servicePath || 'securitycenter.googleapis.com';

  const client = generateClient(servicePath);

  return Promise.resolve()
  .then( () => {
    console.log('requesting cscc to search findings')
    return client.searchFindings({
      orgName: orgName,
      query: 'property.scc_status = "ACTIVE"'
    })
  })
  .catch((error) => {
    console.log(error.error)
    console.log(error)
    return [];
  })
  .then( (response) => {
    if (response && response[0]) {
      console.log('Number of findings found:', response[0].length)
      return response[0];
    }
  });
}

// Upsert a list of findings 
exports.upsertFindings = (sourceFindings, orgName, servicePath) => {
  // getting default values to run unit tests
  servicePath = servicePath || 'securitycenter.googleapis.com';

  const client = generateClient(servicePath);

  return Promise.all(sourceFindings.map(finding => {
      return client.createFinding({
          orgName: orgName,
          sourceFinding: finding
      })
      .catch(err => {
        return (err);
      })
  }));
}
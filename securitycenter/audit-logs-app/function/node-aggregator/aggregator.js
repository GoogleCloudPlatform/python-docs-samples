
var groupBy = require('json-groupby')

const propertiesToExtract = [
  { key: 'insertId', property: 'insertId' },
  { key: 'author', property: 'protoPayload.authenticationInfo.principalEmail' },
  { key: 'resourceType', property: 'resource.type' },
  { key: 'method', property: 'protoPayload.methodName' },
  { key: 'resource', property: 'protoPayload.resourceName' },
  { key: 'deltaPolicy', property: 'protoPayload.serviceData.policyDelta.bindingDeltas' },
  { key: 'labels', property: 'resource.labels' },
  { key: 'timestamp', property: 'timestamp' },
  { key: 'severity', property: 'severity' },
  { key: 'logName', property: 'logName' }
]

exports.aggregate = function (groupedLogs) {
  const aggregated = {};
  for (const key in groupedLogs) {
    createKey(aggregated, key, {});
    let infoList = [];
    let asset = null;
    groupedLogs[key].forEach(log => {
      let info = extractAggregationInfo(log);
      infoList.push(info);
      asset = log.protoPayload.resourceName;
    });
    aggregated[key] = mergeInfo(asset, infoList);
  }
  return aggregated
}

function mergeInfo(resource, infoList) {
  let baseObj = {
    resource: resource,
    ids: groupBy(infoList, ['resource'], ['insertId'])[resource]['insertId'],
    aggregated: infoList
  }
  return baseObj;
}

function extractAggregationInfo(logObj) {
  let resp = {}
  propertiesToExtract.forEach(extractObj => {
    const propertyValue = getPropertyValue(logObj, extractObj.property);
    resp[extractObj.key] = propertyValue;
  });
  return resp;
}

function getPropertyValue(logObj, prop) {
  let value;
  try {
    value = eval(['logObj', prop].join('.'));
  } catch (error) {
    value = null;
  }
  return value;
}

function createKey(obj, key, value) {
  if (!obj[key]) {
    obj[key] = value;
  }
}

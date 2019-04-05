const Finding = require('./finding');
const MOMENT = require('moment');
const groupBy = require('json-groupby')

const READABLE_MESSAGE_V0 = 'readable-message-v0';
const READABLE_MESSAGE_V1 = 'readable-message-v1';
const STRINGIFY_JSON = 'stringify-whole-json';
const GROUP_ACTIONS = 'group-actions';

exports.parseList = function (logObjList, strategy, splitActions) {
  const findings = [];
  for (const key in logObjList) {
    let logObj = logObjList[key];
    findings.push(fromAggregatedLogToFinding(logObj, strategy, splitActions));
  }
  return findings;
}

function fromAggregatedLogToFinding(aggLog, strategy, splitActions) {
  const category = generateCategory(aggLog);
  const protobufTimestamp = generateProtobufTimestamp(MOMENT.utc().valueOf());
  let finding = new Finding(aggLog.ids[0], category, aggLog.resource, protobufTimestamp)
  let aggregated_value = generateAggregate(aggLog.aggregated, strategy);
  finding.addProperty('aggregated_value', aggregated_value);
  finding.addProperty('total_logs_aggregated', aggLog.aggregated.length);
  if (splitActions) {
    let pad = "000000000";
    let strNum = aggregated_value.length + "";
    pad = pad.substring(0, strNum.length + 1)
    for (let i = 0; i < aggregated_value.length; i++) {
      const srtIndex = (i + 1).toString();
      let normalizedValue = pad.substring(0, pad.length - srtIndex.length) + srtIndex;
      finding.addProperty('action_' + normalizedValue, aggregated_value[i]);
    }
  }
  // finding.addProperty('added_roles', aggregated_value.added_roles.join(' /// '));
  // finding.addProperty('removed_roles', aggregated_value.removed_roles.join(' /// '));
  // finding.addProperty('methods', aggregated_value.methods.join(' /// '));
  // finding.addProperty('roles_list', aggregated_value.roles_list.join(' /// '));
  // finding.addProperty('added_actions', aggregated_value.added_actions);
  // finding.addProperty('removed_actions', aggregated_value.removed_actions);
  return finding;
}

function generateAggregate(aggInfo, strategy) {
  if (strategy === STRINGIFY_JSON) {
    return JSON.stringify(aggInfo);
  }
  else {
    normalizedInfo = [];
    // let aggregatedValue = {
    //   added_roles: [],
    //   removed_roles: [],
    //   methods: new Set(),
    //   roles_list: new Set(),
    //   added_actions: null,
    //   removed_actions: null
    // }
    aggInfo.forEach(info => {
      // splittedInfo(info, aggregatedValue);
      let logType = info.method === 'SetIamPolicy' ? info.method : info.resourceType;
      switch (logType) {
        case 'SetIamPolicy':
          normalizedInfo.push(genericAggregator(info, strategy));
          break;
        case 'gcs_bucket':
          normalizedInfo.push(genericAggregator(info, strategy));
          break;
        default:
          break;
      }
    });
    // aggregatedValue.added_actions = aggregatedValue.added_roles.length;
    // aggregatedValue.removed_actions = aggregatedValue.removed_roles.length;
    // aggregatedValue.methods = Array.from(aggregatedValue.methods);
    // aggregatedValue.roles_list = Array.from(aggregatedValue.roles_list);
    // return aggregatedValue;
    return normalizedInfo;
  }
}

function splittedInfo(info, aggregatedValue) {
  let actions = null;
  if (info.deltaPolicy) {
    actions = groupBy(info.deltaPolicy, ['action']);
    for (const key in actions) {
      let aggKey = key === 'REMOVE' ? 'removed_roles' : 'added_roles';
      let messageConnector = key === 'REMOVE' ? ['removed', 'from'] : ['grant', 'to'];
      actions[key].map(action => {
        let message = [info.author, messageConnector[0], action.role, messageConnector[1], action.member, info.timestamp];
        aggregatedValue[aggKey].push(message.join(' '));
        aggregatedValue.roles_list.add(action.role);
        delete action.action;
      });
    }
  }
  aggregatedValue.methods.add(info.method);
}

function genericAggregator(aggInfo, strategy) {
  let actions = null;
  if (aggInfo.deltaPolicy) {
    actions = groupBy(aggInfo.deltaPolicy, ['action']);
    for (const key in actions) {
      actions[key].map(action => {
        delete action.action;
      })
    }
  }

  let labelKeys = Object.keys(aggInfo.labels);
  labelKeys.forEach(key => {
    aggInfo[key] = aggInfo.labels[key];
  });

  delete aggInfo.labels;
  delete aggInfo.deltaPolicy;
  delete aggInfo.resource;
  delete aggInfo.logName;

  aggInfo['actions'] = actions;

  if (strategy === GROUP_ACTIONS) {
    return aggInfo;
  }

  let readableMessage = '';
  let translate = {
    insertId: 'Log ',
    resourceType: ' resource_type:',
    author: ' executed by ',
    method: ' method:',
    timestamp: ' on ',
    severity: ' severity:',
    project_id: ' project:',
    actions: ' actions: ',
    bucket_name: ' bucket_name:',
    location: ' location:'
  }
  if (strategy === READABLE_MESSAGE_V0) {
    for (const key in aggInfo) {
      let stringValue = aggInfo[key];
      if (key === 'actions') {
        stringValue = JSON.stringify(aggInfo[key]);
      }
      readableMessage += translate[key] + stringValue;
    }
    return readableMessage;
  }
  if (strategy === READABLE_MESSAGE_V1) {
    for (const key in aggInfo) {
      let stringValue = aggInfo[key];
      if (key === 'actions') {
        actionString = [];
        for (const actionKey in aggInfo[key]) {
          if (actionKey) {
            actionString.push(actionKey + ' -');
            let infoArray = [];
            actionObj = aggInfo[key][actionKey];
            actionObj.forEach(info => {
              infoArray.push(info.role + ' ' + info.member);
            });
            actionString.push(infoArray.join(', '))
          }
        }
        stringValue = actionString.join(' ');
      }
      if (stringValue) {
        readableMessage += translate[key] + stringValue;
      }
    }
    return readableMessage;
  }
}

function generateCategory(aggLog) {
  let logNames = groupBy(aggLog.aggregated, ['logName']);
  let logNameKeys = Object.keys(logNames);
  if (logNameKeys.length > 1) {
    //TODO: is that an error?
    console.log('More than one log name...');
  } else {
    logName = logNameKeys[0];
  }
  let assetId = normalizeAssetId(aggLog.resource, logName, aggLog.labels)
  let category = ['Aggregated finding', 'assetId:', assetId];
  aggLog.aggregated.forEach(log => {
    addIfNotExist(category, log.method)
  });
  return category.join(' ');
}

function parseProjectId(logName, labels) {
  if (logName.startsWith('projects')) {
    let logNameArray = logName.split("/");
    let projectId = logNameArray[1];
    return projectId
  } else {
    if (labels.hasOwnProperty('project_id')) {
      return labels.project_id;
    }
    return '';
  }
}

function normalizeAssetId(assetId, logName, labels) {
  if (assetId.startsWith('projects/_/')) {
    let projectId = parseProjectId(logName, labels);
    assetId = assetId.replace('projects/_/', 'projects/' + projectId + '/');
  }
  if (assetId.startsWith('projects/')) {
    assetId = assetId.replace('projects/', '');
  }
  return assetId;
}

function addIfNotExist(listObj, valueToAdd) {
  if (listObj.indexOf(valueToAdd) === -1) {
    listObj.push(valueToAdd);
  }
}

function generateProtobufTimestamp(dateInMillis) {
  return {
    seconds: Math.trunc(dateInMillis / 1000),
    nanos: Math.trunc((dateInMillis % 1000) * 1000000)
  }
}
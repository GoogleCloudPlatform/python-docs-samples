'use strict';

const MOMENT = require('moment');
const get = require('get-value');
const RESOURCE_TYPES = require('./resource-types.json');
const uuidv5 = require('uuid/v5');
const SCC_NAMESPACE = '4315c3e6-96e2-4913-9616-67d8fce91297'

const Resource = require('@google-cloud/resource');
const SERVICE_ACCOUNT_KEY_FILE = __dirname + '/accounts/google_api_client.json';

const AUDIT_LOG_TYPE = 'type.googleapis.com/google.cloud.audit.AuditLog';
const IAM_CATEGORY = 'SetIamPolicy';
const BINAUTHZ_CATEGORY = 'io.k8s.core.v1.pods.create';
const BINAUTHZ_CATEGORY_BLOCK = 'BinAuthz blocked deployment attempt';
const BINAUTHZ_CATEGORY_BRAKE_GLASS = 'Breakglass deployment against BinAuthz policy';
const BINAUTHZ_CATEGORY_SUCCESS = 'BinAuthz deployment successful';
const BRAKE_GLASS_ALPHA_PROPERTY_PATH = 'protoPayload.request.metadata.annotations.alpha.image-policy.k8s.io/break-glass';
const BRAKE_GLASS_PROPERTY_PATH = 'labels.imagepolicywebhook.image-policy.k8s.io/break-glass';


function convertWithExtraInfo(logItem, publish) {
    if (logItem.resource.type === "gce_project" || logItem.resource.type === "project") {
        const resource = new Resource({keyFilename: SERVICE_ACCOUNT_KEY_FILE});
        return resource.getProjects({filter:`id:${logItem.resource.labels.project_id}`}).then(results => {
            let realId = logItem.resource.labels.project_id;
            if (results[0] && results[0][0]) {
                realId = results[0][0].metadata.projectNumber;
            }
            let extraInfo = {'resourceName': `//cloudresourcemanager.googleapis.com/projects/${realId}`}
            const finding = convertToFinding(logItem, extraInfo);
            return publish(finding);
        }, err => {
            console.log(err);
            const finding = convertToFinding(logItem, {});
            return publish(finding);
        });
    } else {
        const finding = convertToFinding(logItem, {});
        return publish(finding);
    }
}

function addProperties(baseSourceFinding, logItem) {
    let sourceProperties = {'full_scc_category': baseSourceFinding.category};
    addAll(logItem, sourceProperties, '');
    addSpecificProperties(logItem, sourceProperties);
    baseSourceFinding['sourceProperties'] = sourceProperties;
    return baseSourceFinding;
};

function addSpecificProperties(logObj, baseSourceFinding) {
    const methodName = logObj.protoPayload.methodName;
    const resourceCategory =  methodName === IAM_CATEGORY || methodName === BINAUTHZ_CATEGORY
                                    ? methodName
                                    : logObj.resource.type;
    if (resourceCategory === BINAUTHZ_CATEGORY) {
        addBinAuthSpecificProperties(logObj, baseSourceFinding);
    }
}

function addBinAuthSpecificProperties(logObj, baseSourceFinding) {
    const spec_containers = get(logObj.protoPayload, 'request.spec.containers');
    let images = [];
    spec_containers.map(container => {
        container.image ? images.push(container.image) : null;
    });
    baseSourceFinding.imageNames = JSON.stringify(images);
    if (logObj.protoPayload.response.code === 403) {
        baseSourceFinding.remediation = 'Review image to determine why it was not signed by the required authority prior to deploying. You should also review your Binary Authorization policy to ensure the attestation requirement is correct.';
        const message = get(logObj.protoPayload, 'response.message');
        let { deniedImages, detailedImageInfo, description, denialRule } = arrayOfDeniedImagesAndRawResponseMessage(message);
        baseSourceFinding.description = JSON.stringify(description);
        baseSourceFinding.deniedImageNames = JSON.stringify(deniedImages);
        baseSourceFinding.denialRule = JSON.stringify(denialRule);
        Object.keys(detailedImageInfo).map(key => {
            baseSourceFinding[key] = detailedImageInfo[key];
        });
    }
}

function extractDetailedImageInfo(imagesInfoObject) {
    let contImages = 0;
    let contReasons = 0;
    let detailedImageInfo = {};
    Object.keys(imagesInfoObject).forEach(function (imageName) {
        contReasons = 0;
        detailedImageInfo['image_' + contImages + '_name'] = imageName;
        imagesInfoObject[imageName].forEach(function (reason) {
            detailedImageInfo['image_' + contImages + '_denialRule_' + contReasons] = reason;
            contReasons++;
        });
        contImages++;
    });

    return detailedImageInfo;
}

function arrayOfDeniedImagesAndRawResponseMessage(description) {
    const reasons = description.split('. Image ')
    let imagesInfoObject = {}
    const denialRule = reasons[0]
    reasons.shift(0)

    reasons.map((reason) => {
        reason = reason.replace('Denied by Attestor.', '')
        reason = reason.replace('Denied by Attestor', '')
        reason = reason.replace('Denied by default admission rule.', '')
        reason = reason.replace('Denied by default admission rule', '')
        reason = reason.trim()
        const imageName = reason.split(' ')[0]
        reason = reason.replace(imageName, '')
        if(imagesInfoObject[imageName] == undefined)
            imagesInfoObject[imageName] = [reason.split(' denied by ')[1]]
        else 
            imagesInfoObject[imageName].push(reason.split(' denied by ')[1])
    });
    const deniedImages = Object.keys(imagesInfoObject);
    const detailedImageInfo = extractDetailedImageInfo(imagesInfoObject);
    return {deniedImages, detailedImageInfo, description, denialRule}

}

function cleanName(name){
    return name.replace(/[^A-Za-z0-9_]+/gi,'');
}

function buildSelfLink(logItem){
    let projectId = parseProjectId(logItem);
    let insertId = logItem.insertId;
    return 'https://console.cloud.google.com/logs/viewer?'
    + 'project=' + projectId
    + '&minLogLevel=0&expandAll=true&interval=NO_LIMIT&expandAll=true&advancedFilter=insertId%3D%22'
    + insertId + '%22%0A'
}

function parseProjectId(logItem) {
    if (logItem.logName.startsWith('projects')){
        let logNameArray = logItem.logName.split("/");
        let projectId = logNameArray[1];
        return projectId
    } else {
        if (logItem.resource.labels.hasOwnProperty('project_id')) {
            return logItem.resource.labels.project_id;
        }
        return '';
    }
}

function addAll(baseObj, properties, prefix) {
    for (let property in baseObj) {
        if (baseObj.hasOwnProperty(property)) {
            if (Array.isArray(baseObj[property])) {
                properties[prefix + cleanName(property)] = JSON.stringify(baseObj[property]);
            }
            else {
                if (typeof baseObj[property] === 'object') {
                    addAll(baseObj[property], properties, prefix + property + '_')
                } else {
                    properties[prefix + cleanName(property)] = baseObj[property];
                }
            }
        }
    }
}

function isAuditLog(logItem) {
    return logItem.protoPayload && logItem.protoPayload['@type'] === AUDIT_LOG_TYPE;
}

function normalizedResourceName(logItem) {
    let resourceName = logItem.protoPayload.resourceName;
    let serviceName = logItem.protoPayload.serviceName;
    if (resourceName.startsWith('projects/_/buckets/')) {
        resourceName = resourceName.replace('projects/_/buckets/','');
    }
    const labels = logItem.resource.labels;
    if (labels && labels.cluster_name && labels.project_id && labels.location){
        resourceName = `projects/${labels.project_id}/zones/${labels.location}/clusters/${labels.cluster_name}`;
        serviceName = 'container.googleapis.com'
    }
    if (logItem.resource.type === "dns_managed_zone") {
        resourceName = `projects/${labels.project_id}/managedZones/${labels.zone_name}`
    }
    if (logItem.resource.type === "service_account") {
        resourceName = `projects/${labels.project_id}/serviceAccounts/${labels.unique_id}`
    }
    return '//' + serviceName + '/' + resourceName;
}

function createId(finding) {
    let plainId = finding.resourceName + ':' + finding['sourceProperties'].protoPayload_resourceName + ':' + finding.category + ':' + finding['sourceProperties'].imageNames
    let ids = {"plainId": plainId}
    ids["uuid5"] = uuidv5(plainId, SCC_NAMESPACE).replace(/-/g, '')
    return ids
}

function convertToFinding(logItem, extraInfo) {
    if (isAuditLog(logItem)) {
        const eventTime = MOMENT.utc(logItem.timestamp).format();
        let actualResourceName = '';
        if (extraInfo && extraInfo.resourceName) {
            actualResourceName = extraInfo.resourceName;
        } else {
            actualResourceName = normalizedResourceName(logItem);
        }
        let baseSourceFinding = {
            'state': "ACTIVE",
            'category': generateCategory(logItem),
            'resourceName': actualResourceName,
            'eventTime': eventTime,
            'externalUri': buildSelfLink(logItem)
        };
     
        let sourceFinding = addProperties(baseSourceFinding, logItem);
        if (logItem.protoPayload.methodName === BINAUTHZ_CATEGORY) {
            let ids = createId(sourceFinding)
            sourceFinding['id'] = ids["uuid5"]
            sourceFinding['sourceProperties']['plain_finding_id'] = ids['plainId']
            sourceFinding['sourceProperties']['binaryAuthorization'] = 'true'
        }
        return sourceFinding;
    } else {
        console.log('Invalid log item Received. A log item must have "protoPayload" property to be valid for processing.');
        return null;
    }
 }

function generateCategory(logObj) {
    let category;
    const methodName = logObj.protoPayload.methodName;
    const resourceCategory =  methodName === IAM_CATEGORY || methodName === BINAUTHZ_CATEGORY
                                    ? methodName
                                    : logObj.resource.type;
    switch (resourceCategory) {
        case IAM_CATEGORY:
            category = generateDefaultCategory(logObj, resourceCategory);
            break;
        case BINAUTHZ_CATEGORY:
            category = generateBinauthzCategory(logObj);
            break;
        default:
            category = generateDefaultCategory(logObj, null);
    }
    return category.join(' ');
}

function getAuthor(logObj) {
    if (logObj.protoPayload.authenticationInfo && logObj.protoPayload.authenticationInfo.principalEmail) {
        return logObj.protoPayload.authenticationInfo.principalEmail;
    }
    if (logObj.protoPayload.response && logObj.protoPayload.response.user) {
        return logObj.protoPayload.response.user;
    }

    return 'Authenticated user not found';
}


function generateBinauthzCategory(logObj) {
    let category = []

    if (get(logObj, BRAKE_GLASS_ALPHA_PROPERTY_PATH) || get(logObj, BRAKE_GLASS_PROPERTY_PATH)) {
        category.push(BINAUTHZ_CATEGORY_BRAKE_GLASS);
    } else {
        if (get(logObj, 'protoPayload.response.code') == 403) {
            category.push(BINAUTHZ_CATEGORY_BLOCK);
        } else {
            category.push(BINAUTHZ_CATEGORY_SUCCESS);
        }
    }
    return category;
}

function generateDefaultCategory(logObj, resourceDisplayName) {
    let category = [];

    category.push(defineResourceDisplayName(resourceDisplayName, logObj.resource.type));

    category.push('author:'+ getAuthor(logObj));

    category.push('resourceType:' + logObj.resource.type);

    category.push('methodName:' + logObj.protoPayload.methodName);

    let actionsAndRoles = extractActionsAndRolesFromDelta(logObj);
    if (actionsAndRoles.length) {
        category.push(actionsAndRoles.join(', '));
    }

    let labelKeys = Object.keys(logObj.resource.labels);
    let labelFields = [];
    labelKeys.forEach(key => {
        labelFields.push(key + ':' + logObj.resource.labels[key])
    });
    category.push(labelFields.join(', '));

    return category;
}

function defineResourceDisplayName(resourceDisplayName, resourceType) {
    if (resourceDisplayName) {
        return resourceDisplayName;
    }
    return RESOURCE_TYPES.hasOwnProperty(resourceType) ? RESOURCE_TYPES[resourceType] : resourceType;
}

function extractActionsAndRolesFromDelta(logObj) {
    let actionsAndRoles = [];
    const logServiceData = logObj.protoPayload.serviceData;
    if (logServiceData && logServiceData.policyDelta && logServiceData.policyDelta.bindingDeltas) {
        let deltaList = logServiceData.policyDelta.bindingDeltas
        actionsAndRoles = deltaList.map(delta => {
            return delta.action + ' ' + delta.role + ' ' + delta.member;
        })
    }
    return actionsAndRoles;
}

module.exports.convertWithExtraInfo = convertWithExtraInfo;
module.exports.convertToFinding = convertToFinding;

'use strict';

// Get the stringValue from a property from a given finding
function getFindingPropertyValue(from, propertyName) {
  return from.properties.fields[propertyName] ? from.properties.fields[propertyName].stringValue : null;
}

// Parse Finding into Source_Finding with status property INACTIVE to be updated
function parseSourceFinding(originalFinding) {
  let sourceFinding = {
    id: originalFinding.id,
    sourceId: originalFinding.scannerId,
    assetIds: [ originalFinding.assetId ],
    category: getFindingPropertyValue(originalFinding, 'scc_source_category_id'),
    url: getFindingPropertyValue(originalFinding, 'url'),
    eventTime: {
        seconds: (Number(originalFinding.updateTime.seconds) + 1).toString(),
        nanos: originalFinding.updateTime.nanos
    },
    properties: { fields: {} }
  }

  for (const fieldName in originalFinding.properties.fields) {
    if (fieldName !== 'url') {
      sourceFinding.properties.fields[fieldName] = {
        stringValue: getFindingPropertyValue(originalFinding, fieldName)
      }
    }
  }

  sourceFinding.properties.fields.scc_status = {
    stringValue: 'INACTIVE'
  }

  return sourceFinding;
}

// Iterate over an array of Findings parsing their values to SourceFindings
exports.parseToDeletedSourceFindings = (foundFindings) => {
  let sourceFindings = [];
  foundFindings.forEach(finding => {
      let sourceFinding = parseSourceFinding(finding);
      sourceFindings.push(sourceFinding);
  });

  return sourceFindings;
}
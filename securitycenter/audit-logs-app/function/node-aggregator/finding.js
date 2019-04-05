'use strict';

class Finding {
  constructor (id, category, assetId, eventTime) {
    this.id = 'AUDIT_LOG_' + id;
    this.category = category;
    this.assetIds = [assetId];
    this.sourceId = 'GOOGLE_ANOMALY_DETECTION';
    this.eventTime = eventTime;
    this.properties = {
      fields: {}
    };
  }
  
  addProperty (key, value) {
    this.properties.fields[key] = stringValueObject(value);
  }
}

function stringValueObject(value) {
  return {
    kind: 'stringValue',
    stringValue: value
  }
}

module.exports = Finding;
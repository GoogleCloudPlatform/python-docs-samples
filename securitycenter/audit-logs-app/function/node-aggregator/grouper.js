var groupBy = require('json-groupby')

exports.groupLogs = function(logFileList, propertyToGroup, chunkSize) {
  const groupedList = groupbyProperty(logFileList, propertyToGroup);
  if (chunkSize) {
    return splitChunks(groupedList, chunkSize)
  }
  return groupedList;
}

function splitChunks(groupedList, chunkSize) {
  let finalObj = {}
  for (const key in groupedList) {
    let chunks = createChunks(groupedList[key], chunkSize);
    addChunksToFinalObject(chunks, key, finalObj);
  }
  return finalObj;
}

function groupbyProperty(logFileList, propertyToGroup) {
  return groupBy(logFileList, [propertyToGroup]);
}

function addChunksToFinalObject(chunks, key, finalObj) {
  for (let i = 0; i < chunks.length; i++) {
    objKey = i ? key + '_'  + i : key;
    finalObj[objKey] = chunks[i];
  }
}

function createChunks(originalList, chunkSize) {
  let chunks = [];
  let i,j;
  for (i=0, j = originalList.length; i < j; i += chunkSize) {
    chunks.push(originalList.slice(i, i + chunkSize));
  }
  return chunks;
}
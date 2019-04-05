#!/usr/bin/env node
const JSONStream = require('JSONStream')
const fs = require('fs')
const { Client } = require('scc-client')

const program = require('commander')
const grouper = require('./grouper')
const aggregator = require('./aggregator')
const findingParser = require('./finding-parser')

const PROPERTY_TO_GROUP = 'protoPayload.resourceName'
const MAX_GROUP_SIZE = null
const VALID_STRATEGIES = ['stringify-whole-json', 'group-actions', 'readable-message-v0', 'readable-message-v1']

let logFileList = []

/**
 * Ensure that required options are being passed.
 * @param {*} program commander program
 */
function ensureRequired(program) {
  const validationMessages = []
  program.options.forEach(function (option) {
    const optionName = option.long.replace(/^--/, '')
    if (option.required) {
      if (!program[optionName]) {
        validationMessages.push('Missing ' + option.description + ' with flag ' + option.long)
      }
    }
  })
}

/**
 * Print validation messages
 * @param {*} validationMessages array with violations
 */
function printValidationMessages(validationMessages) {
  if (validationMessages.length > 0) {
    console.log(validationMessages.join('\n'))
    program.help()
  }
}

/**
 * Ensure that the files are present
 * @param {*} files files
 */
function ensureFilePaths(files) {
  const validationMessages = []
  files.forEach(function (file) {
    const filePath = file[0]
    const fileDescription = file[1]
    if (!fs.existsSync(filePath)) {
      validationMessages.push('[' + filePath + '] does not exist. ' +
        fileDescription + ' is required.')
    }
  })
  printValidationMessages(validationMessages)
}

function validateStrategy(program) {
  const validationMessages = []
  if (VALID_STRATEGIES.indexOf(program.strategy) === -1) {
    validationMessages.push('The given strategy: ' + program.strategy + ' is not valid, please select a valid one')
    printValidationMessages(validationMessages)
  }
}

/**
 * Load logs file to memory.
 * @param {*} program from commander
 */
function loadLogFileList() {
  console.log('Starting script')
  console.log('Reading file')
  const fileStream = fs.createReadStream(program.log_file)
  fileStream.pipe(parser)
}

let parser = JSONStream.parse()
  .on('data', data => {
    logFileList.push(data)
  })
  .on('end', () => {
    onFileLoaded()
  })
  .on('error', error => {
    console.log(`PARSE FILE ERROR: ${error}`)
  })

function onFileLoaded() {
  let groupedLogs = grouper.groupLogs(logFileList, PROPERTY_TO_GROUP, MAX_GROUP_SIZE)
  groupedLogs = aggregator.aggregate(groupedLogs)
  const findings = findingParser.parseList(groupedLogs, program.strategy, program.splitActions)
  sendFindingsToSCC(findings).then(resp => {
    console.log('SUCCESS', JSON.stringify(resp))
  }).catch(err => {
    console.log('ERROR', err)
  })
}

function sendFindingsToSCC(findingList) {
  let promiseArray = []

  if (!program.simulation) {
    console.log('Create client')
    client = new Client(program.service_account, program.organization_id, program.api_key)
  }

  findingList.forEach(finding => {
    if (!program.simulation) {
      promiseArray.push(
        client.createFinding(
          program.source_id,
          uuid4().replace(/-/g, ''),
          finding.category,
          finding.state,
          finding.resourceName,
          finding.externalUri,
          finding.sourceProperties,
          finding.securityMarks,
          finding.eventTime)
      )
    } else {
      promiseArray.push(Promise.resolve(finding))
    }
  })

  return Promise.all(promiseArray)
}

program
  .version('0.1.0')
  .description('Aggregate findings from a log file.')
  .option('--no-simulation', 'Execute whole flow without send to SCC')
  .option('--organization_id <organization_id>', 'organization id where the data will be loaded')
  .option('--source_id <source_id>', 'source ID to create findings')
  .option('--service_account <service_account>', 'service account with access to CSCC api')
  .option('--api_key <api_key>', 'api kehy to access CSCC api')
  .option('--log_file <log_file>', 'JSON file with the logs to be aggregated and converted')
  .option('--strategy <strategy>', 'String to define between strategies: stringify-whole-json, group-actions, readable-message-v0, readable-message-v1')
  .option('--split-actions', 'Split each action in one property')
  .parse(process.argv)

ensureRequired(program)
validateStrategy(program)

ensureFilePaths(
  [
    [program.service_account, 'Service account'],
    [program.log_file, 'Log file']
  ]
)

loadLogFileList()
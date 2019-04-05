#!/usr/bin/env node

const program = require('commander');
const fs = require('fs');

const jsonHandler = require('translation/json-handler');
const sender = require('translation/findings-sender');
const yaml = require('js-yaml');

/**
 * Ensure that the files are present
 * @param {*} files files
 */
function ensureFilePaths(files) {
  const validationMessages = [];

  files.forEach(function(file) {
    const filePath = file[0];
    const fileDescription = file[1];
    if (!fs.existsSync(filePath)) {
      validationMessages.push('[' + filePath + '] does not exist. ' +
       fileDescription + ' is required.');
    }
  });

  printValidationMessages(validationMessages);
}

/**
 * Print validation messages
 * @param {*} validationMessages array with violations
 */
function printValidationMessages(validationMessages) {
  if (validationMessages.length > 0) {
    console.log(validationMessages.join('\n'));
    program.help();
  }
}
/**
 * Ensure that required options are being passed.
 * @param {*} program commander program
 */
function ensureRequired(program) {
  const validationMessages = [];
  program.options.forEach(function(option) {
    const optionName = option.long.replace(/^--/, '');
    if (option.required) {
      if (!program[optionName]) {
        validationMessages.push('Missing ' + option.description +
                                ' with flag ' + option.long);
      }
    }
  });

  printValidationMessages(validationMessages);
}

/**
 * Load findings on cscc.
 * @param {*} program from commander
 */
function loadFindings(program) {
  console.log('Real execution');
  const mapper = yaml.safeLoad(fs.readFileSync(program.mapping, 'utf8'));
  const fileStream = fs.createReadStream(program.findings);
  const servicePath = 'securitycenter.googleapis.com';
  const serviceAccount = program.service_account;
  const orgName = 'organizations/' + program.organization_id;

  jsonHandler.handle(fileStream, mapper)
    .then((findings) => sender.sendWithServiceAccount(
      findings,
      orgName,
      servicePath,
      serviceAccount
    ));
}

program
  .version('0.1.0')
  .description('Load findings of a partner on a organization.')
  .option('--no-simulation', 'Really run script')
  .option('--organization_id <organization_id>',
    'organization id where the data will be loaded')
  .option('--service_account <service_account>',
    'service account with access to CSCC api')
  .option('--mapping <mapping>',
    'yaml to map fields from findings.json to CSCC api')
  .option('--findings <findings>', 'JSON file with a list of findings')
  .parse(process.argv);

ensureRequired(program);

ensureFilePaths(
  [
    [program.service_account, 'Service account'],
    [program.mapping, 'Mapping'],
    [program.findings, 'Findings'],
  ]
);

if (!program.simulation) {
  loadFindings(program);
}

console.log('  - %s simulation', program.simulation);
console.log('  - %s organization_id', program.organization_id);
console.log('  - %s service_account', program.service_account);
console.log('  - %s mapping', program.mapping);
console.log('  - %s findings', program.findings);

% SCC Tools: **NodeJS Aggregator Utility**
% Security Cloud Command Center Tools

# Introduction

The objective of this utility is to provide a summarized way to execute the logs aggregation flow avoiding the whole Dataflow proccess.

The NodeJS Aggregator Utility is an command line script that takes a log export json file (expecting the Storage export format) execute all the proccess and transformations to do the aggregation by "asset id" and finnaly saves the generated output on Security Command Center as [findings](https://cloud.google.com/security-command-center/docs/reference/rest/v1alpha3/organizations.findings/create#sourcefinding).

# Requirements

Before start, make sure you have the NodeJs installed at least on version 6.11.0

# Install Dependencies

The script uses a set of dependencies to do all the needed flow and send information to SCC. to install that dependencies access the **script root folder** and run the following command:

```bash
npm install
```
 
# Script execution

Set the environment variables required by the script execution.

**Note:** _You must set them with values that make sense in your context, editing the snippet below before running the commands._

```bash
# the the path to your logs json file.
export log_file=<path_to_file>

# the service account created on the SCC enable project in the organization
# [Help Link](https://cloud.google.com/security-command-center/docs/how-to-programmatic-access)
export scc_service_account=<your_scc_service_account_file>

# the organization id where these scripts will run
export organization_id=<your_org_id>

# the aggregation strategy you want to use, the available untill now are: stringify-whole-json, group-actions, readable-message-v0, readable-message-v1
export strategy=<your_strategy>
```

**Note:** _The script was evolving according SCC Logs Application, so the example below will use the latest strategy defined on project. Please use the flag --help to check the possible options to run the script_

With all needed variables setted and dependencies installed, access the **script root folder** and run the following command:

```bash
node ./index.js --log_file ${log_file} --service_account ${scc_service_account} \
--organization_id ${organization_id} --strategy ${strategy} --split-actions --no-simulation
```


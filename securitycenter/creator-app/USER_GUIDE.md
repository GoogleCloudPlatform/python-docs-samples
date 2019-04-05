% SCC Tools: **Creator** User Guide
% Security Cloud Command Center Tools

\setcounter{section}{0}
\setcounter{secnumdepth}{10}
\newpage

# Operation Modes

The **Creator App** has two operation modes:

* The **Production** mode where a Google App Engine cron job periodically trigger the execution of the stored queries and
* The **Demo** mode where the cron job is ignored and a pub/sub topic message is used to trigger the execution of the stored queries.

The **Creator App** mode can be changed by executing the following instruction:

The user must have the role "Pub/Sub Publisher" at the organization or creator project level.

Install the Python dependencies:

```bash
(cd creator/cli; \
pipenv --python 3.5.3 ; \
pipenv install --ignore-pipfile)
```

Set the application default login:

```bash
gcloud auth application-default login
```

set the mode:

```bash
(cd creator/cli; \
pipenv run python3 load.py mode \
--mode <PRODUCTION|DEMO> \
--project ${creator_project_id} )
```

# Queries

The **Creator App** uses the search_assets and search_findings APIs to retrieve information from Cloud SCC.
Both APIs are restricted to return items from a single organization.

The **Creator App** maps the available parameters passed to the API on the YAML files that contains the queries that are executed by the system.

Sample YAML file with a two-step query example:

```yaml
- name: "Find CLOUDFARE findings on projects owned by dandrade"
  joins:
    - field: name
      kind: ASSET
      order: 1
      type: SINGLE
    - field: resourceName
      kind: FINDING
      order: 2
      type: MULTI
  steps:
    - duration: 43w
      kind: ASSET
      order: 1
      referenceTime:
        type: timestamp
        value: "2018-04-02T10:30:42+0400"
      where: "securityCenterProperties.resourceType = \"google.cloud.resourcemanager.Project\" AND securityCenterProperties.resourceOwners : \"dandrade\""
    - kind: FINDING
      order: 2
      referenceTime:
        type: from_now
        value: 1d+7h+20m
      where: "parent : \"organizations/688851828130/sources/7579907073731359787\""
  threshold:
    operator: gt
    value: 2
  topic: cloudflare_topic
```

On this example we have a query "Find CLOUDFARE findings on projects owned by dandrade" that has two steps: the first one that search projects owned by a user with login "dandrade" and the second one that search findings from CLOUDFLARE on projects found on the first step.

Let's review each part of the example:

* The **name** It is an identifier in human readable form for the query
* The **joins** It is a list to explain which field from the result of the first step should be used to on the second step. Each element contains:
  * An **order** to identify if it is related to the first or second step
  * A **kind** to identify the entity it is related, currently one of ASSET or FINDING
  * The **field** from we are going to extract or construct the join information. Usually in queries with assets and findings it is the asset_id.
  * A **type** that tell us if the field is a scalar value or an array. this is important because if you are extracting information from a **MULTI** field the system needs to split the array in individual values and if you are building the *where* for a step on a **MULTI** field the system needs to use the contains operator ":", instead of the equals operator "=".
* The **steps**: a list with the actual information to be used when calling the asset or findings APIs. Each one contains:
  * The **order** field, to indicate if it is the first or the second step
  * the **kind** field to identify the entity it is related, currently one of ASSET or FINDING. They will be queried against the SCC API.
  * the **where** field with the actual query that will be sent to the API for this step. It can query Attributes, Properties or marks. You can use use the contains operator ":" or the equals operator "=". You can also use AND and OR.
  * **fromLastJobExecution**: An optional field for FINDING steps that will automatically add a restriction to the **where** field value so that only findings created since the last execution of the query will satisfy the original **where** condition. It simulates the simultaneous use of  **referenceTime** and **duration** to set up an interval on the creation time for FINDING steps and will be removed when the **duration** query option becomes available for FINDING steps.
  * **referenceTime** an optional field to represent the moment in time of the search. It has two modes:
    * **TIMESTAMP** mode where you pass a fixed moment in time as a String
    * **FROM_NOW** mode where you pass a time amount.
      * The format is {#weeks}w+{#days}d+{#hours}h+{#minutes}m+{#seconds}s.
      * The moment of the query will be the current date minus the time amount informed.
      * 4w would mean 4\*7\*24\*60\*60 seconds before the current date
      * 3d+4h+15s 3\*24\*60\*60 seconds before the current date
  * **DURATION** an optional field, only valid for the ASSET kind representing a time amount in the form {#weeks}w+{#days}d+{#hours}h+{#minutes}m+{#seconds}s. it will represent an interval before the reference time when the asset existence will be validated.
  * The **threshold** an <operator,value> pair to set a condition on when the result of a query should trigger a message to be posted to the **Notifier App**. This comparison is executed against the size of the response of the last step of the query. The Operator can be one of the following:
    * **lt** lower or equal
    * **le** lower than
    * **eq** equal
    * **ne** not equal
    * **ge** greater or equal
    * **gt** greater than
* The **topic** field,  an optional field with the name of a Pub/sub topic to where the results of this queries should be posted. If not present results will be posted to the default topic. if the topic does not exist it will be created by the application.

## Query examples

The following examples only show the **steps** section of the queries for simplicity.

### Working with datetime type query parameters

1) How can we have a step that will help check if any firewall was created or deleted in a one-hour interval starting 5 minutes before the query execution?

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceType = \"google.compute.Firewall\""
duration: "1h"
referenceTime:
  type: from_now
  value: "5m"
```

This could be used for example to periodically query the API.

2) How to create a step that will check if there was any network created or deleted in the first week of February?

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceType = \"google.compute.Network\""
duration: "1w"
referenceTime:
  type: timestamp
  value: "2018-02-08T00:00:00+0400"
```

### Periodic queries for Finding

1) To periodically query the API for Findings, use the **fromLastJobExecution** option:

```yaml
order: 1
kind: FINDING
where: "category = \"resource_involved_in_coin_mining\""
fromLastJobExecution: "true"
```


## Using Scalar and Multi-value fields

```yaml
order: 1
kind: ASSET
where: "securityCenterProperties.resourceType = \"google.cloud.resourcemanager.Project\" AND securityCenterProperties.resourceOwners : \"dandrade\""
```

**securityCenterProperties.resourceType** is an example of a scalar field and we can use both comparison operators, ':' and '='. The equality operator will do a full match and the ":" will do a substring match in the original value.

**securityCenterProperties.resourceOwners** is an example of a multi-value field.

A sample value could be

```yaml
securityCenterProperties.resourceOwners = ["useralpha@example.com","userbeta@example.com","userga@example.com"]
```

on this case, to be able to query the field value for the user **useralpha** we could do:

```yaml
where: "securityCenterProperties.resourceOwners : \"useralpha@example.com\""
```

this is the available way to query a multi-value attribute for individual values.

## How to test the queries

To update the queries use:

```bash
(cd creator/cli; \
pipenv run python3 load.py event_queries \
--yaml_file <path-to-query-file> \
--project ${creator_project_id})
```

The sample query folder is ./creator/samples, use the one for asset to validate your deploy.

When on "DEMO" mode, to force execution of uploaded queries you need to call the script with 'execute_queries':

```bash
(cd creator/cli; \
pipenv run python3 load.py execute_queries \
--project ${creator_project_id})
```

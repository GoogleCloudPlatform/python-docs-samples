# Tools for connector

Here you can find tools for connector

## Setup

### Node and npm used

* node v8.11.3
* npm 6.1.0

These can be installed with [nvm](https://github.com/creationix/nvm).

```bash
nvm install lts/carbon
```

### Installing dependencies

```bash
npm install
```

## Tools

### load_findings.js

This tool loads findings to an CSCC instance.

It needs these parameters:

* The organization id where the data will be loaded
* A service account from the project with CSCC API enabled on the organization
* A yaml to map fields from findings.json to CSCC api
* A JSON file with a list of findings

#### Using it

The command

```bash
./load_findings.js -h
```

Outputs

```text
  Usage: load_findings [options]

  Load findings of a partner on a organization.

  Options:

    -V, --version                        output the version number
    --no-simulation                      Really run script
    --organization_id <organization_id>  organization id where the data will be loaded
    --service_account <service_account>  service account with access to CSCC api
    --mapping <mapping>                  yaml to map fields from findings.json to CSCC api
    --findings <findings>                JSON file with a list of findings
    -h, --help                           output usage information
```

#### Sample invocation

* Simulation

```bash
export organization_id=123

./load_findings.js \
--organization_id ${organization_id} \
--service_account ~/findings/service_account.json \
--mapping ~/findings/mapping.yaml \
--findings ~/findings/findings.json \
--no-simulation
```

* For real

```bash
export organization_id=123

./load_findings.js \
--organization_id ${organization_id} \
--service_account ~/findings/service_account.json \
--mapping ~/findings/mapping.yaml \
--findings ~/findings/findings.json \
```

## Setup development

This tool follows [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html).
We use [eslint-config-google](https://github.com/google/eslint-config-google) and [eslint](https://eslint.org/) to help with code validation.

### Installing dev dependencies

```bash
npm install -g eslint eslint-config-google
```

### Linting

```bash
eslint *.js
```

### Unit tests

TODO. **PENDING**.
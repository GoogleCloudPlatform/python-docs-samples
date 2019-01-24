
# BigQuery command-line tool

The BigQuery command-line tool is installed as part of the [Cloud SDK](https://cloud-dot-devsite.googleplex.com/sdk/docs/), and can be used to interact with BigQuery using shell commands instead of Python code. Note that shell commands in a notebook must be prepended with a `!`.

## View available commands

To view the available commands for the BigQuery command-line tool, use the `--help` flag.


```python
!bq help
```

    Python script for interacting with BigQuery.
    
    
    USAGE: bq [--global_flags] <command> [--command_flags] [args]
    
    
    Any of the following commands:
      cancel, cp, extract, head, help, init, insert, load, ls, mk, mkdef, partition,
      query, rm, shell, show, update, version, wait
    
    
    cancel     Request a cancel and waits for the job to be cancelled.
    
               Requests a cancel and then either: a) waits until the job is done if
               the sync flag is set [default], or b) returns immediately if the sync
               flag is not set. Not all job types support a cancel, an error is
               returned if it cannot be cancelled. Even for jobs that support a
               cancel, success is not guaranteed, the job may have completed by the
               time the cancel request is noticed, or the job may be in a stage
               where it cannot be cancelled.
    
               Examples:
               bq cancel job_id # Requests a cancel and waits until the job is done.
               bq --nosync cancel job_id # Requests a cancel and returns
               immediately.
    
               Arguments:
               job_id: Job ID to cancel.
    
    cp         Copies one table to another.
    
               Examples:
               bq cp dataset.old_table dataset2.new_table
               bq cp --destination_kms_key=kms_key dataset.old_table
               dataset2.new_table
    
    extract    Perform an extract operation of source_table into destination_uris.
    
               Usage:
               extract <source_table> <destination_uris>
    
               Examples:
               bq extract ds.summary gs://mybucket/summary.csv
    
               Arguments:
               source_table: Source table to extract.
               destination_uris: One or more Google Cloud Storage URIs, separated by
               commas.
    
    head       Displays rows in a table.
    
               Examples:
               bq head dataset.table
               bq head -j job
               bq head -n 10 dataset.table
               bq head -s 5 -n 10 dataset.table
    
    help       Help for all or selected command:
                   bq help [<command>]
    
               To retrieve help with global flags:
                   bq --help
    
               To retrieve help with flags only from the main module:
                   bq --helpshort [<command>]
    
    init       Authenticate and create a default .bigqueryrc file.
    
    insert     Inserts rows in a table.
    
               Inserts the records formatted as newline delimited JSON from file
               into the specified table. If file is not specified, reads from stdin.
               If there were any insert errors it prints the errors to stdout.
    
               Examples:
               bq insert dataset.table /tmp/mydata.json
               echo '{"a":1, "b":2}' | bq insert dataset.table
    
               Template table examples: Insert to dataset.template_suffix table
               using dataset.template table as its template.
               bq insert -x=_suffix dataset.table /tmp/mydata.json
    
    load       Perform a load operation of source into destination_table.
    
               Usage:
               load <destination_table> <source> [<schema>]
    
               The <destination_table> is the fully-qualified table name of table to
               create, or append to if the table already exists.
    
               The <source> argument can be a path to a single local file, or a
               comma-separated list of URIs.
    
               The <schema> argument should be either the name of a JSON file or a
               text schema. This schema should be omitted if the table already has
               one.
    
               In the case that the schema is provided in text form, it should be a
               comma-separated list of entries of the form name[:type], where type
               will default to string if not specified.
    
               In the case that <schema> is a filename, it should contain a single
               array object, each entry of which should be an object with properties
               'name', 'type', and (optionally) 'mode'. See the online documentation
               for more detail:
               https://developers.google.com/bigquery/preparing-data-for-bigquery
    
               Note: the case of a single-entry schema with no type specified is
               ambiguous; one can use name:string to force interpretation as a
               text schema.
    
               Examples:
               bq load ds.new_tbl ./info.csv ./info_schema.json
               bq load ds.new_tbl gs://mybucket/info.csv ./info_schema.json
               bq load ds.small gs://mybucket/small.csv name:integer,value:string
               bq load ds.small gs://mybucket/small.csv field1,field2,field3
    
               Arguments:
               destination_table: Destination table name.
               source: Name of local file to import, or a comma-separated list of
               URI paths to data to import.
               schema: Either a text schema or JSON file, as above.
    
    ls         List the objects contained in the named collection.
    
               List the objects in the named project or dataset. A trailing : or .
               can be used to signify a project or dataset.
               * With -j, show the jobs in the named project.
               * With -p, show all projects.
    
               Examples:
               bq ls
               bq ls -j proj
               bq ls -p -n 1000
               bq ls mydataset
               bq ls -a
               bq ls --filter labels.color:red
               bq ls --filter 'labels.color:red labels.size:*'
               bq ls --transfer_config --transfer_location='us'
               --filter='dataSourceIds:play,adwords'
               bq ls --transfer_run --filter='states:SUCCESSED,PENDING'
               --run_attempt='LATEST' projects/p/locations/l/transferConfigs/c
               bq ls --transfer_log --message_type='messageTypes:INFO,ERROR'
               projects/p/locations/l/transferConfigs/c/runs/r
    
    mk         Create a dataset, table, view, or transfer configuration with this
               name.
    
               See 'bq help load' for more information on specifying the schema.
    
               Examples:
               bq mk new_dataset
               bq mk new_dataset.new_table
               bq --dataset_id=new_dataset mk table
               bq mk -t new_dataset.newtable name:integer,value:string
               bq mk --view='select 1 as num' new_dataset.newview
               (--view_udf_resource=path/to/file.js)
               bq mk -d --data_location=EU new_dataset
               bq mk --transfer_config --target_dataset=dataset --display_name=name
               -p='{"param":"value"}' --data_source=source
               bq mk --transfer_run --start_time={start_time} --end_time={end_time}
               projects/p/locations/l/transferConfigs/c
    
    mkdef      Emits a definition in JSON for a GCS backed table.
    
               The output of this command can be redirected to a file and used for
               the external_table_definition flag with the "bq query" and "bq mk"
               commands. It produces a definition with the most commonly used values
               for options. You can modify the output to override option values.
    
               Usage:
               mkdef <source_uris> [<schema>]
    
               Examples:
               bq mkdef 'gs://bucket/file.csv' field1:integer,field2:string
    
               Arguments:
               source_uris: a comma-separated list of uris.
               schema: The <schema> argument should be either the name of a JSON
               file or
               a text schema.
    
               In the case that the schema is provided in text form, it should be a
               comma-separated list of entries of the form name[:type], where type
               will
               default to string if not specified.
    
               In the case that <schema> is a filename, it should contain a
               single array object, each entry of which should be an object with
               properties 'name', 'type', and (optionally) 'mode'. See the online
               documentation for more detail:
               https://developers.google.com/bigquery/preparing-data-for-bigquery
    
               Note: the case of a single-entry schema with no type specified is
               ambiguous; one can use name:string to force interpretation as a
               text schema.
    
    partition  Copies source tables into partitioned tables.
    
               Usage: bq partition <source_table_prefix>
               <destination_partitioned_table>
    
               Copies tables of the format <source_table_prefix><YYYYmmdd> to a
               destination partitioned table, with the date suffix of the source
               tables becoming the partition date of the destination table
               partitions.
    
               If the destination table does not exist, one will be created with a
               schema and that matches the last table that matches the supplied
               prefix.
    
               Examples:
               bq partition dataset1.sharded_ dataset2.partitioned_table
    
    query      Execute a query.
    
               Query should be specifed on command line, or passed on stdin.
    
               Examples:
               bq query 'select count(*) from publicdata:samples.shakespeare'
               echo 'select count(*) from publicdata:samples.shakespeare' | bq query
    
               Usage:
               query [<sql_query>]
    
    rm         Delete the dataset, table, or transfer config described by
               identifier.
    
               Always requires an identifier, unlike the show and ls commands. By
               default, also requires confirmation before deleting. Supports the -d
               -t flags to signify that the identifier is a dataset or table.
               * With -f, don't ask for confirmation before deleting.
               * With -r, remove all tables in the named dataset.
    
               Examples:
               bq rm ds.table
               bq rm -r -f old_dataset
               bq rm --transfer_config=projects/p/locations/l/transferConfigs/c
    
    shell      Start an interactive bq session.
    
    show       Show all information about an object.
    
               Examples:
               bq show -j <job_id>
               bq show dataset
               bq show [--schema] dataset.table
               bq show [--view] dataset.view
               bq show --transfer_config projects/p/locations/l/transferConfigs/c
               bq show --transfer_run
               projects/p/locations/l/transferConfigs/c/runs/r
               bq show --encryption_service_account
    
    update     Updates a dataset, table, view or transfer configuration with this
               name.
    
               See 'bq help load' for more information on specifying the schema.
    
               Examples:
               bq update --description "Dataset description" existing_dataset
               bq update --description "My table" existing_dataset.existing_table
               bq update -t existing_dataset.existing_table
               name:integer,value:string
               bq update --destination_kms_key
               projects/p/locations/l/keyRings/r/cryptoKeys/k
               existing_dataset.existing_table
               bq update --view='select 1 as num' existing_dataset.existing_view
               (--view_udf_resource=path/to/file.js)
               bq update --transfer_config --display_name=name
               -p='{"param":"value"}'
               projects/p/locations/l/transferConfigs/c
               bq update --transfer_config --target_dataset=dataset
               --refresh_window_days=5 --update_credentials
               projects/p/locations/l/transferConfigs/c
    
    version    Return the version of bq.
    
    wait       Wait some number of seconds for a job to finish.
    
               Poll job_id until either (1) the job is DONE or (2) the specified
               number of seconds have elapsed. Waits forever if unspecified. If no
               job_id is specified, and there is only one running job, we poll that
               job.
    
               Examples:
               bq wait # Waits forever for the currently running job.
               bq wait job_id # Waits forever
               bq wait job_id 100 # Waits 100 seconds
               bq wait job_id 0 # Polls if a job is done, then returns immediately.
               # These may exit with a non-zero status code to indicate "failure":
               bq wait --fail_on_error job_id # Succeeds if job succeeds.
               bq wait --fail_on_error job_id 100 # Succeeds if job succeeds in 100
               sec.
    
               Arguments:
               job_id: Job ID to wait on.
               secs: Number of seconds to wait (must be >= 0).
    
    
    Run 'bq --help' to get help for global flags.
    Run 'bq help <command>' to get help for <command>.


## Create a new dataset

A dataset is contained within a specific [project](https://cloud.google.com/bigquery/docs/projects). Datasets are top-level containers that are used to organize and control access to your [tables](https://cloud.google.com/bigquery/docs/tables) and [views](https://cloud.google.com/bigquery/docs/views). A table or view must belong to a dataset, so you need to create at least one dataset before [loading data into BigQuery](https://cloud.google.com/bigquery/loading-data-into-bigquery).

The example below creates a new dataset in the US named "your_new_dataset".


```python
!bq --location=US mk --dataset "your_dataset_id"
```

    Dataset 'your-project-id:your_dataset_id' successfully created.


## Load data from a local file to a table

The example below demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Loading Data into BigQuery from a Local Data Source](https://cloud.google.com/bigquery/docs/loading-data-local) in the BigQuery documentation.


```python
!bq load --help
```

    Python script for interacting with BigQuery.
    
    
    USAGE: bq [--global_flags] <command> [--command_flags] [args]
    
    
    load       Perform a load operation of source into destination_table.
    
               Usage:
               load <destination_table> <source> [<schema>]
    
               The <destination_table> is the fully-qualified table name of table to
               create, or append to if the table already exists.
    
               The <source> argument can be a path to a single local file, or a
               comma-separated list of URIs.
    
               The <schema> argument should be either the name of a JSON file or a
               text schema. This schema should be omitted if the table already has
               one.
    
               In the case that the schema is provided in text form, it should be a
               comma-separated list of entries of the form name[:type], where type
               will default to string if not specified.
    
               In the case that <schema> is a filename, it should contain a single
               array object, each entry of which should be an object with properties
               'name', 'type', and (optionally) 'mode'. See the online documentation
               for more detail:
               https://developers.google.com/bigquery/preparing-data-for-bigquery
    
               Note: the case of a single-entry schema with no type specified is
               ambiguous; one can use name:string to force interpretation as a
               text schema.
    
               Examples:
               bq load ds.new_tbl ./info.csv ./info_schema.json
               bq load ds.new_tbl gs://mybucket/info.csv ./info_schema.json
               bq load ds.small gs://mybucket/small.csv name:integer,value:string
               bq load ds.small gs://mybucket/small.csv field1,field2,field3
    
               Arguments:
               destination_table: Destination table name.
               source: Name of local file to import, or a comma-separated list of
               URI paths to data to import.
               schema: Either a text schema or JSON file, as above.
    
               Flags for load:
    
    /Users/ajhamilton/google-cloud-sdk/platform/bq/bq.py:
      --[no]allow_jagged_rows: Whether to allow missing trailing optional columns in
        CSV import data.
      --[no]allow_quoted_newlines: Whether to allow quoted newlines in CSV import
        data.
      --[no]autodetect: Enable auto detection of schema and options for formats that
        are not self describing like CSV and JSON.
      --clustering_fields: Comma separated field names. Can only be specified with
        time based partitioning. Data will be first partitioned and subsequently
        "clustered on these fields.
      --destination_kms_key: Cloud KMS key for encryption of the destination table
        data.
      -E,--encoding: <UTF-8|ISO-8859-1>: The character encoding used by the input
        file. Options include:
        ISO-8859-1 (also known as Latin-1)
        UTF-8
      -F,--field_delimiter: The character that indicates the boundary between
        columns in the input file. "\t" and "tab" are accepted names for tab.
      --[no]ignore_unknown_values: Whether to allow and ignore extra, unrecognized
        values in CSV or JSON import data.
      --max_bad_records: Maximum number of bad records allowed before the entire job
        fails.
        (default: '0')
        (an integer)
      --null_marker: An optional custom string that will represent a NULL valuein
        CSV import data.
      --projection_fields: If sourceFormat is set to "DATASTORE_BACKUP", indicates
        which entity properties to load into BigQuery from a Cloud Datastore backup.
        Property names are case sensitive and must refer to top-level properties.
        (default: '')
        (a comma separated list)
      --quote: Quote character to use to enclose records. Default is ". To indicate
        no quote character at all, use an empty string.
      --[no]replace: If true erase existing contents before loading new data.
        (default: 'false')
      --[no]require_partition_filter: Whether to require partition filter for
        queries over this table. Only apply to partitioned table.
      --schema: Either a filename or a comma-separated list of fields in the form
        name[:type].
      --schema_update_option: Can be specified when append to a table, or replace a
        table partition. When specified, the schema of the destination table will be
        updated with the schema of the new data. One or more of the following
        options can be specified:
        ALLOW_FIELD_ADDITION: allow new fields to be added
        ALLOW_FIELD_RELAXATION: allow relaxing required fields to nullable;
        repeat this option to specify a list of values
      --skip_leading_rows: The number of rows at the beginning of the source file to
        skip.
        (an integer)
      --source_format:
        <CSV|NEWLINE_DELIMITED_JSON|DATASTORE_BACKUP|AVRO|PARQUET|ORC>: Format of
        source data. Options include:
        CSV
        NEWLINE_DELIMITED_JSON
        DATASTORE_BACKUP
        AVRO
        PARQUET
        ORC (experimental)
      --time_partitioning_expiration: Enables time based partitioning on the table
        and sets the number of seconds for which to keep the storage for the
        partitions in the table. The storage in a partition will have an expiration
        time of its partition time plus this value. A negative number means no
        expiration.
        (an integer)
      --time_partitioning_field: Enables time based partitioning on the table and
        the table will be partitioned based on the value of this field. If time
        based partitioning is enabled without this value, the table will be
        partitioned based on the loading time.
      --time_partitioning_type: Enables time based partitioning on the table and set
        the type. The only type accepted is DAY, which will generate one partition
        per day.
    
    gflags:
      --flagfile: Insert flag definitions from the given file into the command line.
        (default: '')
      --undefok: comma-separated list of flag names that it is okay to specify on
        the command line even if the program does not define a flag with that name.
        IMPORTANT: flags in this list that have arguments MUST use the --flag=value
        format.
        (default: '')
    
    
    Global flags:
    
    bq_auth_flags:
      --application_default_credential_file: Only for the gcloud wrapper use.
        (default: '')
      --credential_file: Only for the gcloud wrapper use.
        (default: '/Users/ajhamilton/.bigquery.v2.token')
      --service_account: Only for the gcloud wrapper use.
        (default: '')
      --service_account_credential_file: Only for the gcloud wrapper use.
      --service_account_private_key_file: Only for the gcloud wrapper use.
        (default: '')
      --service_account_private_key_password: Only for the gcloud wrapper use.
        (default: 'notasecret')
      --[no]use_gce_service_account: Only for the gcloud wrapper use.
        (default: 'false')
    
    bq_flags:
      --api: API endpoint to talk to.
        (default: 'https://www.googleapis.com')
      --api_version: API version to use.
        (default: 'v2')
      --apilog: Log all API requests and responses to the file specified by this
        flag. Also accepts "stdout" and "stderr". Specifying the empty string will
        direct to stdout.
      --bigqueryrc: Path to configuration file. The configuration file specifies new
        defaults for any flags, and can be overrridden by specifying the flag on the
        command line. If the --bigqueryrc flag is not specified, the BIGQUERYRC
        environment variable is used. If that is not specified, the path
        "~/.bigqueryrc" is used.
        (default: '/Users/ajhamilton/.bigqueryrc')
      --ca_certificates_file: Location of CA certificates file.
        (default: '')
      --dataset_id: Default dataset reference to use for requests (Ignored when not
        applicable.). Can be set as "project:dataset" or "dataset". If project is
        missing, the value of the project_id flag will be used.
        (default: '')
      --[no]debug_mode: Show tracebacks on Python exceptions.
        (default: 'false')
      --[no]disable_ssl_validation: Disables HTTPS certificates validation. This is
        off by default.
        (default: 'false')
      --discovery_file: Filename for JSON document to read for discovery.
        (default: '')
      --[no]enable_gdrive: When set to true, requests new OAuth token with GDrive
        scope. When set to false, requests new OAuth token without GDrive scope.
      --[no]fingerprint_job_id: Whether to use a job id that is derived from a
        fingerprint of the job configuration. This will prevent the same job from
        running multiple times accidentally.
        (default: 'false')
      --format: <none|json|prettyjson|csv|sparse|pretty>: Format for command output.
        Options include:
        pretty: formatted table output
        sparse: simpler table output
        prettyjson: easy-to-read JSON format
        json: maximally compact JSON
        csv: csv format with header
        The first three are intended to be human-readable, and the latter three are
        for passing to another program. If no format is selected, one will be chosen
        based on the command run.
      --[no]headless: Whether this bq session is running without user interaction.
        This affects behavior that expects user interaction, like whether debug_mode
        will break into the debugger and lowers the frequency of informational
        printing.
        (default: 'false')
      --httplib2_debuglevel: Instruct httplib2 to print debugging messages by
        setting debuglevel to the given value.
      --job_id: A unique job_id to use for the request. If not specified, this
        client will generate a job_id. Applies only to commands that launch jobs,
        such as cp, extract, load, and query.
      --job_property: Additional key-value pairs to include in the properties field
        of the job configuration;
        repeat this option to specify a list of values
      --location: Default geographic location to use when creating datasets or
        determining where jobs should run (Ignored when not applicable.)
      --max_rows_per_request: Specifies the max number of rows to return per read.
        (an integer)
      --project_id: Default project to use for requests.
        (default: '')
      --proxy_address: The name or IP address of the proxy host to use for
        connecting to GCP.
        (default: '')
      --proxy_password: The password to use when authenticating with proxy host.
        (default: '')
      --proxy_port: The port number to use to connect to the proxy host.
        (default: '')
      --proxy_username: The user name to use when authenticating with proxy host.
        (default: '')
      -q,--[no]quiet: If True, ignore status updates while jobs are running.
        (default: 'false')
      -sync,--[no]synchronous_mode: If True, wait for command completion before
        returning, and use the job completion status for error codes. If False,
        simply create the job, and use the success of job creation as the error
        code.
        (default: 'true')
      --trace: A tracing token of the form "token:<token>" to include in api
        requests.
    
    google.apputils.app:
      -?,--[no]help: show this help
      --[no]helpshort: show usage only for this module
      --[no]helpxml: like --help, but generates XML output
      --[no]run_with_pdb: Set to true for PDB debug mode
        (default: 'false')
      --[no]run_with_profiling: Set to true for profiling the script. Execution will
        be slower, and the output format might change over time.
        (default: 'false')
      --[no]show_build_data: show build data and exit
      --[no]use_cprofile_for_profiling: Use cProfile instead of the profile module
        for profiling. This has no effect unless --run_with_profiling is set.
        (default: 'true')
    
    gflags:
      --flagfile: Insert flag definitions from the given file into the command line.
        (default: '')
      --undefok: comma-separated list of flag names that it is okay to specify on
        the command line even if the program does not define a flag with that name.
        IMPORTANT: flags in this list that have arguments MUST use the --flag=value
        format.
        (default: '')
    
    Run 'bq help' to see the list of available commands.



```python
!bq --location=US load --autodetect --skip_leading_rows=1 --source_format=CSV your_dataset_id.us_states_local_file 'resources/us-states.csv'
```

    Upload complete.
    Waiting on bqjob_r42e105decd46e2a1_0000016880baeb55_1 ... (0s) Current status: DONE   


## Load data from Google Cloud Storage to a table

The example below demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Introduction to Loading Data from Cloud Storage](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage) in the BigQuery documentation.


```python
!bq --location=US load --autodetect --skip_leading_rows=1 --source_format=CSV your_dataset_id.us_states_gcs 'gs://cloud-samples-data/bigquery/us-states/us-states.csv'
```

    Waiting on bqjob_r52ccf09d3eb8c617_0000016880bb0711_1 ... (2s) Current status: DONE   


## Run a query

The BigQuery command-line tool has a `query` command for running queries, but it is recommended to use the [Magic command](./BigQuery%20Query%20Magic.ipynb) for this purpose.

## Cleaning Up

The following code deletes the dataset created for this tutorial, including all tables in the dataset.


```python
!bq rm -r -f --dataset your_dataset_id
```

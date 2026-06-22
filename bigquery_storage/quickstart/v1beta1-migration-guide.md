# Migrating BigQuery Storage API from v1beta1 to v1: Python

This guide shows how to migrate Python code using the BigQuery Storage API from
version `v1beta1` to `v1`.

## Key Changes

*   **Package Imports**: `google.cloud.bigquery_storage_v1beta1` ->
    `google.cloud.bigquery_storage_v1`
*   **Service Client**: `BigQueryStorageClient` is replaced by
    `BigQueryReadClient`.
*   **Table Reference**: `TableReference` type is replaced by a simple string
    representation of the table path in `ReadSession.table`.
*   **Session Configuration**: Configuration fields (table, format, read
    options) have moved into `ReadSession` type, which is passed in
    `CreateReadSessionRequest`.
*   **Parallelism**: `requested_streams` parameter in `create_read_session` is
    replaced by `max_stream_count`.
*   **Sharding Strategy**: `sharding_strategy` is removed. The server now
    automatically balances the streams.
*   **Read Rows Request**: `StreamPosition` is flattened. You now pass the
    stream name directly to `read_rows`.

## Code Comparison

### 1. Client Initialization

**v1beta1:**

```python
from google.cloud import bigquery_storage_v1beta1

client = bigquery_storage_v1beta1.BigQueryStorageClient()
```

**v1:**

```python
from google.cloud import bigquery_storage_v1

client = bigquery_storage_v1.BigQueryReadClient()
```

### 2. Creating a Read Session

**v1beta1:**

```python
from google.cloud import bigquery_storage_v1beta1

table_ref = bigquery_storage_v1beta1.types.TableReference()
table_ref.project_id = "bigquery-public-data"
table_ref.dataset_id = "usa_names"
table_ref.table_id = "usa_1910_current"

read_options = bigquery_storage_v1beta1.types.TableReadOptions()
read_options.selected_fields.append("name")
read_options.row_restriction = 'state = "WA"'

session = client.create_read_session(
    table_reference=table_ref,
    parent='projects/read-session-project',
    read_options=read_options,
    requested_streams=1,
    format=bigquery_storage_v1beta1.types.DataFormat.AVRO,
    sharding_strategy=bigquery_storage_v1beta1.types.ShardingStrategy.LIQUID
)
```

**v1:**

```python
from google.cloud import bigquery_storage_v1

# Table path is now a string: projects/{project}/datasets/{dataset}/tables/{table}
table_path = "projects/bigquery-public-data/datasets/usa_names/tables/usa_1910_current"

read_options = bigquery_storage_v1.types.ReadSession.TableReadOptions()
read_options.selected_fields.append("name")
read_options.row_restriction = 'state = "WA"'

# ReadSession holds the session configuration
read_session = bigquery_storage_v1.types.ReadSession(
    table=table_path,
    data_format=bigquery_storage_v1.types.DataFormat.AVRO, # format renamed to data_format
    read_options=read_options
)

session = client.create_read_session(
    parent="projects/read-session-project",
    read_session=read_session,
    max_stream_count=1 # requested_streams renamed to max_stream_count
)
```

### 3. Reading Rows

**v1beta1:**

```python
from google.cloud import bigquery_storage_v1beta1

position = bigquery_storage_v1beta1.types.StreamPosition(
    stream=session.streams[0]
)

reader = client.read_rows(read_position=position)

for row in reader.rows(session):
    print(row["name"])
```

**v1:**

```python
# read_rows accepts stream name and offset directly.
# Note that the parameter name in the library helper is 'name', which maps to 'read_stream' in proto.
reader = client.read_rows(session.streams[0].name)

# In v1, you don't need to pass session to rows() if schema info is already present,
# but the client library handles it.
for row in reader.rows():
    print(row["name"])
```

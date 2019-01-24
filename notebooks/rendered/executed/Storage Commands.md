
# Storage Commands

The [Google Cloud SDK](https://cloud-dot-devsite.googleplex.com/sdk/docs/) provides a set of commands for working with data stored in Google Cloud Storage.

This notebook introduces several `gsutil` commands for interacting with Cloud Storage.

## List available commands

The `gsutil` command can be used to perform a wide array of tasks. Run the `help` command to view a list of available commands:


```python
!gsutil help
```

    Usage: gsutil [-D] [-DD] [-h header]... [-m] [-o] [-q] [command [opts...] args...]
    Available commands:
      acl             Get, set, or change bucket and/or object ACLs
      cat             Concatenate object content to stdout
      compose         Concatenate a sequence of objects into a new composite object.
      config          Obtain credentials and create configuration file
      cors            Get or set a CORS JSON document for one or more buckets
      cp              Copy files and objects
      defacl          Get, set, or change default ACL on buckets
      defstorageclass Get or set the default storage class on buckets
      du              Display object size usage
      hash            Calculate file hashes
      help            Get help about commands and topics
      iam             Get, set, or change bucket and/or object IAM permissions.
      kms             Configure Cloud KMS encryption
      label           Get, set, or change the label configuration of a bucket.
      lifecycle       Get or set lifecycle configuration for a bucket
      logging         Configure or retrieve logging on buckets
      ls              List providers, buckets, or objects
      mb              Make buckets
      mv              Move/rename objects and/or subdirectories
      notification    Configure object change notification
      perfdiag        Run performance diagnostic
      rb              Remove buckets
      requesterpays   Enable or disable requester pays for one or more buckets
      retention       Provides utilities to interact with Retention Policy feature.
      rewrite         Rewrite objects
      rm              Remove objects
      rsync           Synchronize content of two buckets/directories
      setmeta         Set metadata on already uploaded objects
      signurl         Create a signed url
      stat            Display object status
      test            Run gsutil unit/integration tests (for developers)
      update          Update to the latest gsutil release
      version         Print version info about gsutil
      versioning      Enable or suspend versioning for one or more buckets
      web             Set a main page and/or error page for one or more buckets
    
    Additional help topics:
      acls            Working With Access Control Lists
      anon            Accessing Public Data Without Credentials
      apis            Cloud Storage APIs
      crc32c          CRC32C and Installing crcmod
      creds           Credential Types Supporting Various Use Cases
      dev             Contributing Code to gsutil
      encoding        Filename encoding and interoperability problems
      encryption      Using Encryption Keys
      metadata        Working With Object Metadata
      naming          Object and Bucket Naming
      options         Top-Level Command-Line Options
      prod            Scripting Production Transfers
      projects        Working With Projects
      retries         Retry Handling Strategy
      security        Security and Privacy Considerations
      subdirs         How Subdirectories Work
      support         Google Cloud Storage Support
      throttling      Throttling gsutil
      versions        Object Versioning and Concurrency Control
      wildcards       Wildcard Names
    
    Use gsutil help <command or topic> for detailed help.

## Buckets

Buckets are the basic containers that hold your data. Everything that you
store in Cloud Storage must be contained in a bucket. You can use buckets to
organize your data and control access to your data.

### Create a bucket

When you [create a bucket](https://cloud.google.com/storage/docs/creating-buckets),
you specify a globally-unique name.


```python
# Replace the string below with a unique name for the new bucket
bucket_name = 'your-new-bucket'
```

NOTE: In the examples below, the variables are referenced in the command using `$` and `{}`. You may replace the interpolated variables with literal values if they are constant instead of creating and using variables.


```python
!gsutil mb gs://{bucket_name}/
```

    Creating gs://your-new-bucket/...


### List buckets in a project

Replace 'your-project-id' in the cell below with your project ID and run the cell to list the storage buckets in your project.


```python
!gsutil ls -p your-project-id
```

    gs://your-project-id/
    gs://my-new-bucket-1548180688764/
    gs://my-new-bucket-1548208228513/
    gs://test-storage-bucket-1548209987490/
    gs://your-new-bucket/


## Objects

Objects are the individual pieces of data that you store in Cloud Storage.
There is no limit on the number of objects that you can create in a bucket.

### Upload a local file to a bucket


```python
!gsutil cp resources/us-states.txt gs://{bucket_name}/
```

    Copying file://resources/us-states.txt [Content-Type=text/plain]...
    
    Operation completed over 1 objects/637.0 B.                                      


### List blobs in a bucket


```python
!gsutil ls -r gs://{bucket_name}/**
```

    gs://your-new-bucket/us-states.txt


### Get a blob and display metadata
See [documentation](https://cloud.google.com/storage/docs/viewing-editing-metadata) for more information about object metadata.


```python
!gsutil ls -L  gs://{bucket_name}/us-states.txt
```

    gs://your-new-bucket/us-states.txt:
        Creation time:          Thu, 24 Jan 2019 16:40:54 GMT
        Update time:            Thu, 24 Jan 2019 16:40:54 GMT
        Storage class:          STANDARD
        Content-Language:       en
        Content-Length:         637
        Content-Type:           text/plain
        Hash (crc32c):          AmYMRQ==
        Hash (md5):             NmfddAHdCzyvAHCifeGtwg==
        ETag:                   CO63hf7thuACEAE=
        Generation:             1548348054133742
        Metageneration:         1
        ACL:                    [
      {
        "entity": "project-owners-129776587519",
        "projectTeam": {
          "projectNumber": "129776587519",
          "team": "owners"
        },
        "role": "OWNER"
      },
      {
        "entity": "project-editors-129776587519",
        "projectTeam": {
          "projectNumber": "129776587519",
          "team": "editors"
        },
        "role": "OWNER"
      },
      {
        "entity": "project-viewers-129776587519",
        "projectTeam": {
          "projectNumber": "129776587519",
          "team": "viewers"
        },
        "role": "READER"
      },
      {
        "email": "ajhamilton@google.com",
        "entity": "user-ajhamilton@google.com",
        "role": "OWNER"
      }
    ]
    TOTAL: 1 objects, 637 bytes (637 B)


### Download a blob to a local directory


```python
!gsutil cp gs://{bucket_name}/us-states.txt resources/downloaded-us-states.txt
```

    Copying gs://your-new-bucket/us-states.txt...
    
    Operation completed over 1 objects/637.0 B.                                      


## Cleaning up

### Delete a blob


```python
!gsutil rm gs://{bucket_name}/us-states.txt
```

    Removing gs://your-new-bucket/us-states.txt...
    
    Operation completed over 1 objects.                                              


### Delete a bucket


```python
!gsutil rm -r gs://{bucket_name}/
```

    Removing gs://your-new-bucket/...


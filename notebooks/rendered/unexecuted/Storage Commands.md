
# Storage Commands

The [Google Cloud SDK](https://cloud-dot-devsite.googleplex.com/sdk/docs/) provides a set of commands for working with data stored in Google Cloud Storage.

This notebook introduces several `gsutil` commands for interacting with Cloud Storage.

## List available commands

The `gsutil` command can be used to perform a wide array of tasks. Run the `help` command to view a list of available commands:


```python
!gsutil help
```

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

### List buckets in a project

Replace 'your-project-id' in the cell below with your project ID and run the cell to list the storage buckets in your project.


```python
!gsutil ls -p your-project-id
```

## Objects

Objects are the individual pieces of data that you store in Cloud Storage.
There is no limit on the number of objects that you can create in a bucket.

### Upload a local file to a bucket


```python
!gsutil cp resources/us-states.txt gs://{bucket_name}/
```

### List blobs in a bucket


```python
!gsutil ls -r gs://{bucket_name}/**
```

### Get a blob and display metadata
See [documentation](https://cloud.google.com/storage/docs/viewing-editing-metadata) for more information about object metadata.


```python
!gsutil ls -L  gs://{bucket_name}/us-states.txt
```

### Download a blob to a local directory


```python
!gsutil cp gs://{bucket_name}/us-states.txt resources/downloaded-us-states.txt
```

## Cleaning up

### Delete a blob


```python
!gsutil rm gs://{bucket_name}/us-states.txt
```

### Delete a bucket


```python
!gsutil rm -r gs://{bucket_name}/
```

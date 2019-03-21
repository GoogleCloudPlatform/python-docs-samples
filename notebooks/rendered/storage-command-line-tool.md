
# Storage command-line tool

The [Google Cloud SDK](https://cloud-dot-devsite.googleplex.com/sdk/docs/) provides a set of commands for working with data stored in Cloud Storage. This notebook introduces several `gsutil` commands for interacting with Cloud Storage. Note that shell commands in a notebook must be prepended with a `!`.

## List available commands

The `gsutil` command can be used to perform a wide array of tasks. Run the `help` command to view a list of available commands:


```python
!gsutil help
```

## Create a storage bucket

Buckets are the basic containers that hold your data. Everything that you store in Cloud Storage must be contained in a bucket. You can use buckets to organize your data and control access to your data.

Start by defining a globally unique name.

For more information about naming buckets, see [Bucket name requirements](https://cloud.google.com/storage/docs/naming#requirements).


```python
# Replace the string below with a unique name for the new bucket
bucket_name = "your-new-bucket"
```

NOTE: In the examples below, the `bucket_name`  and `project_id` variables are referenced in the commands using `{}` and `$`. If you want to avoid creating and using variables, replace these interpolated variables with literal values and remove the `{}` and `$` characters.

Next, create the new bucket with the `gsutil mb` command:


```python
!gsutil mb gs://{bucket_name}/
```

## List buckets in a project

Replace 'your-project-id' in the cell below with your project ID and run the cell to list the storage buckets in your project.


```python
# Replace the string below with your project ID
project_id = "your-project-id"
```


```python
!gsutil ls -p $project_id
```

The response should look like the following:

```
gs://your-new-bucket/
```

## Get bucket metadata

The next cell shows how to get information on metadata of your Cloud Storage buckets.

To learn more about specific bucket properties, see [Bucket locations](https://cloud.google.com/storage/docs/locations) and [Storage classes](https://cloud.google.com/storage/docs/storage-classes).


```python
!gsutil ls -L -b gs://{bucket_name}/
```

The response should look like the following:
```
gs://your-new-bucket/ :
  Storage class:         MULTI_REGIONAL
  Location constraint:   US
  ...
```

## Upload a local file to a bucket

Objects are the individual pieces of data that you store in Cloud Storage. Objects are referred to as "blobs" in the Python client library. There is no limit on the number of objects that you can create in a bucket.

An object's name is treated as a piece of object metadata in Cloud Storage. Object names can contain any combination of Unicode characters (UTF-8 encoded) and must be less than 1024 bytes in length.

For more information, including how to rename an object, see the [Object name requirements](https://cloud.google.com/storage/docs/naming#objectnames).


```python
!gsutil cp resources/us-states.txt gs://{bucket_name}/
```

## List blobs in a bucket


```python
!gsutil ls -r gs://{bucket_name}/**
```

The response should look like the following:
```
gs://your-new-bucket/us-states.txt
```

## Get a blob and display metadata

See [Viewing and editing object metadata](https://cloud.google.com/storage/docs/viewing-editing-metadata) for more information about object metadata.


```python
!gsutil ls -L  gs://{bucket_name}/us-states.txt
```

The response should look like the following:

```
gs://your-new-bucket/us-states.txt:
    Creation time:          Fri, 08 Feb 2019 05:23:28 GMT
    Update time:            Fri, 08 Feb 2019 05:23:28 GMT
    Storage class:          STANDARD
    Content-Language:       en
    Content-Length:         637
    Content-Type:           text/plain
...
```

## Download a blob to a local directory


```python
!gsutil cp gs://{bucket_name}/us-states.txt resources/downloaded-us-states.txt
```

## Cleaning up

### Delete a blob


```python
!gsutil rm gs://{bucket_name}/us-states.txt
```

### Delete a bucket

The following command deletes all objects in the bucket before deleting the bucket itself.


```python
!gsutil rm -r gs://{bucket_name}/
```

## Next Steps

Read more about Cloud Storage in the documentation:
+ [Storage key terms](https://cloud.google.com/storage/docs/key-terms)
+ [How-to guides](https://cloud.google.com/storage/docs/how-to)
+ [Pricing](https://cloud.google.com/storage/pricing)



```python
%matplotlib inline
```


```python
%load_ext google.cloud.bigquery
```

# Google Cloud Storage

This page shows how to get started with the Google Cloud Storage Python client library.

## Import the library


```python
from google.cloud import storage
```

## Projects

All data in Cloud Storage belongs inside a project. A project consists of a
set of users, a set of APIs, and billing, authentication, and monitoring
settings for those APIs. You can have one project or multiple projects.

## Clients
Start by initializing a client, which is used to interact with the Google Cloud Storage API. The project used by the client will default to the project associated with your credentials. Alternatively, you can explicitly specify a project when constructing the client.


```python
client = storage.Client(project="ajhamilton-scratch")
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
bucket_name = 'test-storage-bucket-1548268970715'

# Creates the new bucket
bucket = client.create_bucket(bucket_name)

print('Bucket {} created.'.format(bucket.name))
```

    Bucket test-storage-bucket-1548268970715 created.


### List buckets in a project


```python
buckets = client.list_buckets()

print("Buckets in {}:".format(client.project))
for item in buckets:
    print("\t" + item.name)
```

    Buckets in ajhamilton-scratch:
    	ajhamilton-scratch
    	my-new-bucket-1548180688764
    	my-new-bucket-1548208228513
    	test-storage-bucket-1548209987490
    	test-storage-bucket-1548268970715


### Get a bucket


```python
bucket = client.get_bucket(bucket_name)
```

## Objects

Objects are the individual pieces of data that you store in Cloud Storage.
There is no limit on the number of objects that you can create in a bucket.

### Upload a local file to a bucket


```python
blob_name = 'us-states.txt'
blob = bucket.blob(blob_name)

source_file_name = 'resources/us-states.txt'
blob.upload_from_filename(source_file_name)

print('File uploaded to {}.'.format(bucket.name))
```

    File uploaded to test-storage-bucket-1548268970715.


### List blobs in a bucket


```python
blobs = bucket.list_blobs()

print("Blobs in {}:".format(bucket.name))
for item in blobs:
    print("\t" + item.name)
```

    Blobs in test-storage-bucket-1548268970715:
    	us-states.txt


### Get a blob and display metadata
See [documentation](https://cloud.google.com/storage/docs/viewing-editing-metadata) for more information about object metadata.


```python
blob = bucket.get_blob(blob_name)

print('Select metadata for blob {}:'.format(blob_name))
print('\tID: {}'.format(blob.id))
print('\tSize: {} bytes'.format(blob.size))
print('\tUpdated: {}'.format(blob.updated))
```

    Select metadata for blob us-states.txt:
    	ID: test-storage-bucket-1548268970715/us-states.txt/1548268974850839
    	Size: 637 bytes
    	Updated: 2019-01-23 18:42:54.850000+00:00


### Download a blob to a local directory


```python
output_file_name = 'resources/downloaded-us-states.txt'
blob.download_to_filename(output_file_name)

print('Downloaded blob {} to {}.'.format(blob.name, output_file_name))
```

    Downloaded blob us-states.txt to resources/downloaded-us-states.txt.


## Cleaning up

### Delete a blob


```python
blob = client.get_bucket(bucket_name).get_blob(blob_name)
blob.delete()

print('Blob {} deleted.'.format(blob.name))
```

    Blob us-states.txt deleted.


### Delete a bucket


```python
bucket = client.get_bucket(bucket_name)
bucket.delete()

print('Bucket {} deleted.'.format(bucket.name))
```

    Bucket test-storage-bucket-1548268970715 deleted.


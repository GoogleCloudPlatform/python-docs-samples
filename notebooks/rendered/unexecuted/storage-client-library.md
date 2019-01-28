
# Google Cloud Storage

This page shows how to get started with the [Google Cloud Storage Python client library](https://googleapis.github.io/google-cloud-python/latest/storage/index.html).

## Create a storage bucket

Buckets are the basic containers that hold your data. Everything that you store in Cloud Storage must be contained in a bucket. You can use buckets to organize your data and control access to your data.

Start by importing the library:


```python
from google.cloud import storage
```

Next, initialize a client object, which is used to interact with the Google Cloud Storage API. The project used by the client will default to the project associated with the credentials file stored in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

See the [google-auth](https://google-auth.readthedocs.io/en/latest/reference/google.auth.html) for more information about Application Default Credentials.

Run the following to create a client with your default project:


```python
client = storage.Client()
print("Client creating using default project: {}".format(client.project))
```

Alternatively, you can explicitly specify a project when constructing the client:


```python
client = storage.Client(project="your-project-id")
```

Finally, create a bucket with a globally unique name.


```python
# Replace the string below with a unique name for the new bucket
bucket_name = 'your-new-bucket'

# Creates the new bucket
bucket = client.create_bucket(bucket_name)

print('Bucket {} created.'.format(bucket.name))
```

For more information, see [Creating Storage Buckets](https://cloud.google.com/storage/docs/creating-buckets) in the Cloud Storage documentation.

### List buckets in a project


```python
buckets = client.list_buckets()

print("Buckets in {}:".format(client.project))
for item in buckets:
    print("\t" + item.name)
```

### Get bucket metadata


```python
bucket = client.get_bucket(bucket_name)
```

## Objects

Objects are the individual pieces of data that you store in Cloud Storage. There is no limit on the number of objects that you can create in a bucket.

An object's name is treated as a piece of object metadata in Cloud Storage. Object names can contain any combination of Unicode characters (UTF-8 encoded) and must be less than 1024 bytes in length.

Though data in storage buckets is stored similar to a local file system, Google Cloud Storage is a key/value pair object store. A common character to include in object names to emulate directory structure is a slash (/). By using slashes, you can make objects appear as though they're stored in a hierarchical structure. For example, you could name one object `/europe/france/paris.jpg` and another object `/europe/france/cannes.jpg`. When you list these objects, they appear to be in a hierarchical directory structure based on location; however, Cloud Storage sees the objects as independent with no hierarchical relationship whatsoever.

For more information, including how to rename an object, see the [object naming guidelines](https://cloud.google.com/storage/docs/naming#objectnames).

### Upload a local file to a bucket


```python
blob_name = 'us-states.txt'
blob = bucket.blob(blob_name)

source_file_name = 'resources/us-states.txt'
blob.upload_from_filename(source_file_name)

print('File uploaded to {}.'.format(bucket.name))
```

### List blobs in a bucket


```python
blobs = bucket.list_blobs()

print("Blobs in {}:".format(bucket.name))
for item in blobs:
    print("\t" + item.name)
```

### Get a blob and display metadata
See [documentation](https://cloud.google.com/storage/docs/viewing-editing-metadata) for more information about object metadata.


```python
blob = bucket.get_blob(blob_name)

print('Select metadata for blob {}:'.format(blob_name))
print('\tID: {}'.format(blob.id))
print('\tSize: {} bytes'.format(blob.size))
print('\tUpdated: {}'.format(blob.updated))
```

### Download a blob to a local directory


```python
output_file_name = 'resources/downloaded-us-states.txt'
blob.download_to_filename(output_file_name)

print('Downloaded blob {} to {}.'.format(blob.name, output_file_name))
```

## Cleaning up

### Delete a blob


```python
blob = client.get_bucket(bucket_name).get_blob(blob_name)
blob.delete()

print('Blob {} deleted.'.format(blob.name))
```

### Delete a bucket


```python
bucket = client.get_bucket(bucket_name)
bucket.delete()

print('Bucket {} deleted.'.format(bucket.name))
```

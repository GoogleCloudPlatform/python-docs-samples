
# Cloud Storage client library

This tutorial shows how to get started with the [Cloud Storage Python client library](https://googleapis.github.io/google-cloud-python/latest/storage/index.html).

## Create a storage bucket

Buckets are the basic containers that hold your data. Everything that you store in Cloud Storage must be contained in a bucket. You can use buckets to organize your data and control access to your data.

Start by importing the library:


```python
from google.cloud import storage
```

The `storage.Client` object uses your default project. Alternatively, you can specify a project in the `Client` constructor. For more information about how the default project is determined, see the [google-auth documentation](https://google-auth.readthedocs.io/en/latest/reference/google.auth.html).

Run the following to create a client with your default project:


```python
client = storage.Client()
print("Client created using default project: {}".format(client.project))
```

To explicitly specify a project when constructing the client, set the `project` parameter:


```python
# client = storage.Client(project='your-project-id')
```

Finally, create a bucket with a globally unique name.

For more information about naming buckets, see [Bucket name requirements](https://cloud.google.com/storage/docs/naming#requirements).


```python
# Replace the string below with a unique name for the new bucket
bucket_name = "your-new-bucket"

# Creates the new bucket
bucket = client.create_bucket(bucket_name)

print("Bucket {} created.".format(bucket.name))
```

## List buckets in a project


```python
buckets = client.list_buckets()

print("Buckets in {}:".format(client.project))
for item in buckets:
    print("\t" + item.name)
```

## Get bucket metadata

The next cell shows how to get information on metadata of your Cloud Storage buckets.

To learn more about specific bucket properties, see [Bucket locations](https://cloud.google.com/storage/docs/locations) and [Storage classes](https://cloud.google.com/storage/docs/storage-classes).


```python
bucket = client.get_bucket(bucket_name)

print("Bucket name: {}".format(bucket.name))
print("Bucket location: {}".format(bucket.location))
print("Bucket storage class: {}".format(bucket.storage_class))
```

## Upload a local file to a bucket

Objects are the individual pieces of data that you store in Cloud Storage. Objects are referred to as "blobs" in the Python client library. There is no limit on the number of objects that you can create in a bucket.

An object's name is treated as a piece of object metadata in Cloud Storage. Object names can contain any combination of Unicode characters (UTF-8 encoded) and must be less than 1024 bytes in length.

For more information, including how to rename an object, see the [Object name requirements](https://cloud.google.com/storage/docs/naming#objectnames).


```python
blob_name = "us-states.txt"
blob = bucket.blob(blob_name)

source_file_name = "resources/us-states.txt"
blob.upload_from_filename(source_file_name)

print("File uploaded to {}.".format(bucket.name))
```

## List blobs in a bucket


```python
blobs = bucket.list_blobs()

print("Blobs in {}:".format(bucket.name))
for item in blobs:
    print("\t" + item.name)
```

## Get a blob and display metadata

See [documentation](https://cloud.google.com/storage/docs/viewing-editing-metadata) for more information about object metadata.


```python
blob = bucket.get_blob(blob_name)

print("Name: {}".format(blob.id))
print("Size: {} bytes".format(blob.size))
print("Content type: {}".format(blob.content_type))
print("Public URL: {}".format(blob.public_url))
```

## Download a blob to a local directory


```python
output_file_name = "resources/downloaded-us-states.txt"
blob.download_to_filename(output_file_name)

print("Downloaded blob {} to {}.".format(blob.name, output_file_name))
```

## Cleaning up

### Delete a blob


```python
blob = client.get_bucket(bucket_name).get_blob(blob_name)
blob.delete()

print("Blob {} deleted.".format(blob.name))
```

### Delete a bucket

Note that the bucket must be empty before it can be deleted.


```python
bucket = client.get_bucket(bucket_name)
bucket.delete()

print("Bucket {} deleted.".format(bucket.name))
```

## Next Steps

Read more about Cloud Storage in the documentation:
+ [Storage key terms](https://cloud.google.com/storage/docs/key-terms)
+ [How-to guides](https://cloud.google.com/storage/docs/how-to)
+ [Pricing](https://cloud.google.com/storage/pricing)

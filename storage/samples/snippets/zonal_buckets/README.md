# Google Cloud Storage - Zonal Buckets Snippets

This directory contains snippets for interacting with Google Cloud Storage zonal buckets.

## Prerequisites

- A Google Cloud Platform project with the Cloud Storage API enabled.
- A zonal Google Cloud Storage bucket.

## Running the snippets

### Create and write to an appendable object

This snippet uploads an appendable object to a zonal bucket.

```bash
python samples/snippets/zonal_buckets/storage_create_and_write_appendable_object.py --bucket_name <bucket_name> --object_name <object_name>
```

### Finalize an appendable object upload

This snippet creates, writes to, and finalizes an appendable object.

```bash
python samples/snippets/zonal_buckets/storage_finalize_appendable_object_upload.py --bucket_name <bucket_name> --object_name <object_name>
```

### Pause and resume an appendable object upload

This snippet demonstrates pausing and resuming an appendable object upload.

```bash
python samples/snippets/zonal_buckets/storage_pause_and_resume_appendable_upload.py --bucket_name <bucket_name> --object_name <object_name>
```

### Tail an appendable object

This snippet demonstrates tailing an appendable GCS object, similar to `tail -f`.

```bash
python samples/snippets/zonal_buckets/storage_read_appendable_object_tail.py --bucket_name <bucket_name> --object_name <object_name> --duration <duration_in_seconds>
```


### Download a range of bytes from an object

This snippet downloads a range of bytes from an object.

```bash
python samples/snippets/zonal_buckets/storage_open_object_single_ranged_read.py --bucket_name <bucket_name> --object_name <object_name> --start_byte <start_byte> --size <size>
```


### Download multiple ranges of bytes from a single object

This snippet downloads multiple ranges of bytes from a single object into different buffers.

```bash
python samples/snippets/zonal_buckets/storage_open_object_multiple_ranged_read.py --bucket_name <bucket_name> --object_name <object_name>
```

### Download the entire content of an object

This snippet downloads the entire content of an object using a multi-range downloader.

```bash
python samples/snippets/zonal_buckets/storage_open_object_read_full_object.py --bucket_name <bucket_name> --object_name <object_name>
```



### Download a range of bytes from multiple objects concurrently

This snippet downloads a range of bytes from multiple objects concurrently.

```bash
python samples/snippets/zonal_buckets/storage_open_multiple_objects_ranged_read.py --bucket_name <bucket_name> --object_names <object_name_1> <object_name_2>
```
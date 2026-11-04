# Google Cloud Storage - Bidirectional Streaming (Bidi) Snippets

This directory contains snippets that use the Google Cloud Storage gRPC
bidirectional streaming (bidi) APIs, including appendable object writes and
multi-range reads.

## Prerequisites

- A Google Cloud Platform project with the Cloud Storage API enabled.
- For the appendable object snippets (create, finalize, pause and resume, tail,
  and the pre-warmed writer pool), a rapid bucket (a bucket with the Rapid
  storage class).
- The ranged read snippets work with any Google Cloud Storage bucket.

## Running the snippets

### Create and write to an appendable object

This snippet uploads an appendable object to a rapid bucket.

```bash
python samples/snippets/bidi/storage_create_and_write_appendable_object.py --bucket_name <bucket_name> --object_name <object_name>
```

### Finalize an appendable object upload

This snippet creates, writes to, and finalizes an appendable object.

```bash
python samples/snippets/bidi/storage_finalize_appendable_object_upload.py --bucket_name <bucket_name> --object_name <object_name>
```

### Pause and resume an appendable object upload

This snippet demonstrates pausing and resuming an appendable object upload.

```bash
python samples/snippets/bidi/storage_pause_and_resume_appendable_upload.py --bucket_name <bucket_name> --object_name <object_name>
```

### Tail an appendable object

This snippet demonstrates tailing an appendable GCS object, similar to `tail -f`.

```bash
python samples/snippets/bidi/storage_read_appendable_object_tail.py --bucket_name <bucket_name> --object_name <object_name> --duration <duration_in_seconds>
```


### Download a range of bytes from an object

This snippet downloads a range of bytes from an object.

```bash
python samples/snippets/bidi/storage_open_object_single_ranged_read.py --bucket_name <bucket_name> --object_name <object_name> --start_byte <start_byte> --size <size>
```


### Download multiple ranges of bytes from a single object

This snippet downloads multiple ranges of bytes from a single object into different buffers.

```bash
python samples/snippets/bidi/storage_open_object_multiple_ranged_read.py --bucket_name <bucket_name> --object_name <object_name>
```

### Download the entire content of an object

This snippet downloads the entire content of an object using a multi-range downloader.

```bash
python samples/snippets/bidi/storage_open_object_read_full_object.py --bucket_name <bucket_name> --object_name <object_name>
```



### Download a range of bytes from multiple objects concurrently

This snippet downloads a range of bytes from multiple objects concurrently.

```bash
python samples/snippets/bidi/storage_open_multiple_objects_ranged_read.py --bucket_name <bucket_name> --object_names <object_name_1> <object_name_2>
```

### Optimize write latency with a pre-warmed writer pool

This snippet uses a pre-warmed pool of writers for appendable objects in a rapid bucket.

```bash
python samples/snippets/bidi/storage_optimize_write_latency_pool.py --bucket_name <bucket_name> --key_prefix <key_prefix>
```
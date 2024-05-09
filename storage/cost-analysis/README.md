# Cloud Storage Python Samples

===============================================================================

[![Open in Cloud Shell button](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/s3-sdk/README.rst)

**Cloud Storage** https://cloud.google.com/storage/docs

## Samples

NOTE: Due to the specific functionality related to Google Cloud APIs, this guide
assumes a base level of familiarity with the Cloud Storage features,
terminology, and pricing.

## Cloud Storage Soft Delete Cost Analyzer

### Purpose

*   Helps you understand the potential cost implications of enabling
    [Soft Delete](https://cloud.google.com/storage/docs/soft-delete) on your
    Cloud Storage [buckets](https://cloud.google.com/storage/docs/buckets).
*   Identifies buckets where the cost of enabling soft delete exceeds some
    threshold based on past usage.

### Prerequisites

*   A
    [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
    with existing buckets.
*   Permissions on your Google Cloud project to interact with Cloud Storage and
    Monitoring APIs.
*   A [Python development environment](https://cloud.google.com/python/setup)
    with version >= `3.11`

### Running the script using the command line

To disable soft-delete for buckets flagged by the script, follow these steps:

1.  Authenticate (if needed): If you're not already authenticated or prefer a
    specific account, run:

    ```code-block::bash
    gcloud auth application-default login
    ```

2.  Run the analyzer to generate a list of buckets exceeding your cost
    threshold:

    ```code-block::bash
    python storage_soft_delete_relative_cost_analyzer.py [project_name] --[OTHER_OPTIONS] --list=True > list_of_buckets.txt
    ```

    ARGUMENTS:

    *   `project_name` - (**Required**): Specifies your Google Cloud project
        name.
    *   `--cost_threshold` - (Optional, default=0): Sets a relative cost
        threshold. For example, if `cost_threshold` is set to 0.15, the script
        will return buckets where the estimated relative cost increase exceeds
        15%.
    *   `--soft_delete_window` - (Optional, default= 604800.0 (i.e. 7 days)):
        Time window (in seconds) for considering soft-deleted objects.
    *   `--agg_days` - (Optional, default=30): The period over which to combine
        and aggregate results.
    *   `--lookback_days` - (Optional, default=360): Time window (in days) which
        describes how far back in time the analysis should consider data.
    *   `--list` - (Optional, default=False): Produces a simple list of bucket
        names if set as True.

    Example with all the optional parameters set to their default values:

    ```code-block::bash
    python storage_soft_delete_relative_cost_analyzer.py [project_name] \
        --cost_threshold=0 \
        --soft_delete_window=604800.0 \
        --agg_days=30 \
        --lookback_days=360 \
        --list=true
    ```

3.  Update the buckets using the generated list:

    ```code-block::bash
    cat list_of_buckets.txt | gcloud storage buckets update -I --clear-soft-delete
    ```

**Important Note** <span style="color: red;">If a bucket has soft delete
disabled, delete requests that include an object's generation number will
permanently delete the object. Additionally, any request in buckets with object
versioning disabled that cause an object to be deleted or overwritten will
permanently delete the object.</span>

--------------------------------------------------------------------------------

### Script Explanation

The `storage_soft_delete_relative_cost_analyzer.py` script assesses the
potential cost impact of enabling soft delete on Cloud Storage buckets. It uses
the [Cloud Monitoring API](https://cloud.google.com/monitoring/api/v3) to
retrieve relevant metrics and perform calculations.

#### Functionality

1.  Calculates the relative cost of soft delete:

    *   Fetches data on soft-deleted bytes and total byte-seconds for each
        bucket and
        [storage class](https://cloud.google.com/storage/docs/storage-classes)
        using the Monitoring API.
    *   Calculates the ratio of soft-deleted bytes to total byte-seconds,
        representing the relative amount of inactive data.
    *   Considers
        [storage class pricing](https://cloud.google.com/storage/pricing) is
        relative to the Standard storage class to determine the cost impact of
        storing this inactive data.

2.  Identifies buckets that exceed a cost threshold:

    *   Compares the calculated relative cost to a user-defined threshold.
    *   Flags buckets where soft delete might lead to significant cost
        increases.

3.  Provides two different output options: JSON or list of buckets.

    *   Can output a detailed JSON with relative cost for each bucket, suitable
        for further analysis or plotting.
    *   Alternatively, generates a simple list of bucket names exceeding the
        cost threshold. This output can be directly piped into the gcloud
        storage CLI as described above.

#### Key Functions

*   `soft_delete_relative_cost_analyzer`: Handles command-line input and output,
    calling 'get_soft_delete_cost' for the Google Cloud project.
    *   `get_soft_delete_cost`: Orchestrates the cost analysis, using:
        *   `get_relative_cost`: Retrieves the relative cost multiplier for a
            given storage class (e.g., "STANDARD", "NEARLINE") compared to the
            standard class. The cost for each class are pre-defined within the
            function and could be adjusted based on regional pricing variations.
        *   `calculate_soft_delete_costs`: Executes Monitoring API queries and
            calculates costs.
        *   `get_storage_class_ratio`: Fetches data on storage class
            distribution within buckets.

#### Monitoring API Queries

The script relies on the Cloud Monitoring API to fetch essential data for
calculating soft delete costs. It employs the `query_client.query_time_series`
method to execute specifically crafted queries that retrieve metrics from Cloud
Storage.

1.  `calculate_soft_delete_costs`

    *   This function calculates the proportion of soft-deleted data relative to
        the total data volume within each bucket. The calculation is based on
        the following metrics:
        *   `storage.googleapis.com/storage/v2/deleted_bytes`: This metric
            quantifies the volume of data, in bytes, that has undergone soft
            deletion.
        *   `storage.googleapis.com/storage/v2/total_byte_seconds`: This metric
            records the cumulative byte-seconds of data stored within the
            bucket, excluding objects marked for soft deletion.

2.  `get_storage_class_ratio`

    *   This function uses a query to re-acquire the
        `storage.googleapis.com/storage/v2/total_byte_seconds` metric. However,
        in this instance, it focuses on segregating and aggregating the data
        based on the storage class associated with each object within the
        bucket.
    *   The resultant output is a distribution of data across various storage
        classes, facilitating a more granular cost analysis. For example, a
        result like `{ "bucket_name-STANDARD": 0.90, "bucket_name-NEARLINE":
        0.10 }` indicates that the bucket's data is stored across two storage
        classes with a ratio of 9:1.

--------------------------------------------------------------------------------

### Key Formula

The relative increase in cost of using soft delete is calculated by combining
the output of above mentioned queries and the for each bucket,

```
Relative cost of each bucket = deleted_bytes / total_byte_seconds
                                 x Soft delete retention duration-seconds
                                 x Relative Storage Cost
                                 x Storage Class Ratio
```

where,

*   `Deleted Bytes`: It is same as `storage/v2/deleted_bytes`. Delta count of
    deleted bytes per bucket.
*   `Total Bytes Seconds`: It is same as `storage/v2/total_byte_seconds`. Total
    daily storage in byte*seconds used by the bucket, grouped by storage class
    and type where type can be live-object, noncurrent-object,
    soft-deleted-object and multipart-upload.
*   `Soft delete retention duration-seconds`: Soft Delete window defined for the
    bucket, this is the threshold to be provided to test out this relative cost
    script.
*   `Relative Storage Cost`: The cost of storing data in a specific storage
    class (e.g., Standard, Nearline, Coldline) relative to the Standard class
    (where Standard class cost is 1).
*   `Storage Class Ratio`: The proportion of the bucket's data that belongs to
    the specific storage class being considered.

Please note the following Cloud Monitoring metrics: `storage/v2/deleted_bytes`
and `storage/v2/total_byte_seconds` are defined on
[https://cloud.google.com/monitoring/api/metrics_gcp#gcp-storage](https://cloud.google.com/monitoring/api/metrics_gcp#gcp-storage)

#### Stepwise Explanation

1.  Soft Delete Rate: Dividing 'Deleted Bytes' by 'Total Bytes Seconds' gives
    you the rate at which data is being soft-deleted (per second). This shows
    how quickly data marked for deletion accumulates in the bucket.
2.  Cost Impact:
    *   Multiply the `Soft Delete Rate` by the `Soft delete retention
        duration-seconds` to get the total ratio of data that is soft-deleted
        and retained within the specified period.
    *   Multiply this result by the 'Relative Storage Cost` to factor in the
        pricing of the specific storage class.
    *   Finally, multiply by the `Storage Class Ratio` to consider only the
        portion of the cost attributable to that particular class.

A script analyzes your bucket usage history to estimate the relative cost
increase of enabling soft delete. It outputs a fraction for each bucket,
representing the fractional increase in cost compared to current pricing if
usage patterns continue. For instance, `{"Bucket_A": 1.15,"Bucket_B": 1.05}`
indicates a `15%` price increase for `Bucket_A` and `5%` increase for `Bucket_B`
with soft delete enabled for the defined `Soft delete retention
duration-seconds`. This output allows you to weigh the benefits of data
protection against the added storage expenses for each bucket and storage class,
helping you make informed decisions about enabling soft delete.

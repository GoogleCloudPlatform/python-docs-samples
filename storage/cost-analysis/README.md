Google Cloud Storage Python Samples
===============================================================================

[![Open in Cloud Shell button](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/s3-sdk/README.rst)

**Google Cloud Storage:** https://cloud.google.com/storage/docs 

Samples
-------------------------------------------------------------------------------
NOTE: Due to the specific functionality related to Google Cloud APIs, this guide assumes a base level of familiarity with Google Cloud Storage features, terminology, and pricing.

### Google Cloud Storage Soft Delete Cost Analyzer
-------------------------------------------------------------------------------
**Purpose**

* Helps you understand the potential cost implications of enabling soft delete on your Google Cloud Storage buckets.
* Identifies buckets where soft delete might lead to significant cost increases.

**Key Concepts**
   1. Soft Delete: A feature for protecting against accidental data loss. Deleted objects are retained for a defined period before permanent deletion. This adds safety but carries potential additional storage costs.
   2. Cost Analysis: This script evaluates the relative cost increase within each bucket if soft delete is enabled. Considerations include:
        * Your soft delete retention period
        * Amount of data likely to be soft-deleted
        * Proportions of data in different storage classes (e.g., Standard, Nearline)

**How to Use**

**Prerequisites**

     1. A Google Cloud Platform (GCP) Project with existing buckets.
     2. Permissions on your GCP project to interact with Google Cloud Storage and Monitoring APIs.
     3. A Python environment (https://cloud.google.com/python/setup) [ Python version > Python 3.11.6 ]

**Command-Line Arguments**
* `project_name` - (**Required**): Specifies your GCP project name.
* `--cost_threshold` - (Optional, default=0): Sets a relative cost threshold.
* `--soft_delete_window` - (Optional, default= 604800.0 (i.e. 7 days)): Time window (in seconds) for considering soft-deleted objects..
* `--agg_days` - (Optional, default=30): The period over which to combine and aggregate results.
* `--lookback_days` - (Optional, default=360): Time window (in days) for considering the how old the bucket to be.
* `--list` - (Optional, default=False): Produces a simple list of bucket names if set as True.

Note: In this sample, if setting cost_threshold 0.15 would spotlight buckets where enabling soft delete might increase costs by over 15%.

``` code-block:: bash
    $ python storage_soft_delete_relative_cost_analyzer.py [your-project-name] 
```

To disable soft-delete for buckets flagged by the script, follow these steps:

```code-block::bash
# 1. Authenticate (if needed): If you're not already authenticated or prefer a specific account, run:
gcloud auth application-default login

# 2. Run the analyzer to generate a list of buckets exceeding your cost threshold:
python storage_soft_delete_relative_cost_analyzer.py [your-project-name] --[OTHER_OPTIONS] --list=True > list_of_buckets.txt

# 3. Update the buckets using the generated list:
cat list_of_buckets.txt | gcloud storage buckets update -I --clear-soft-delete

```

**Important Note:** <span style="color: red;">Disabling soft-delete for flagged buckets means when deleting it will permanently delete files. These files cannot be restored, even if a soft-delete policy is later re-enabled.</span> 

-------------------------------------------------------------------------------

### SCRIPT EXPLAINATION
The `storage_soft_delete_relative_cost_analyzer.py` script assesses the potential cost impact of enabling soft delete on Google Cloud Storage buckets. It utilizes the Google Cloud Monitoring API to retrieve relevant metrics and perform calculations.

#### Functionality:

1. Calculating Relative Soft Delete Cost:
   * Fetches data on soft-deleted bytes and total byte-seconds for each bucket and storage class using the Monitoring API.
   * Calculates the ratio of soft-deleted bytes to total byte-seconds, representing the relative amount of inactive data.
   * Considers storage class pricing to determine the cost impact of storing this inactive data.

2. Identifying Costly Buckets:

   * Compares the calculated relative cost to a user-defined threshold.
   * Flags buckets where soft delete might lead to significant cost increases.
     
3. Output Options:
   
   * Can output a detailed JSON report with cost data for each bucket, suitable for further analysis or plotting.
   * Alternatively, generates a simple list of bucket names exceeding the cost threshold.

#### Key Functions:

   * `soft_delete_relative_cost_analyzer`: Handles command-line input and output, calling 'get_soft_delete_cost' for the project.
     
      * `get_soft_delete_cost`: Orchestrates the cost analysis, using:
        
         * `get_relative_cost`: Retrieves the relative cost multiplier for a given storage class (e.g., "STANDARD", "NEARLINE") compared to the standard class. The cost for each class are pre-defined within the function and could be adjusted based on regional pricing variations.
         * `calculate_soft_delete_costs`: Executes Monitoring API queries and calculates costs.
         * `get_storage_class_ratio`: Fetches data on storage class distribution within buckets.

#### Monitoring API Queries

The script relies on the Google Cloud Monitoring API to fetch essential data for calculating soft delete costs. It employs the `query_client.query_time_series` method to execute specifically crafted queries that retrieve metrics from Google Cloud Storage.

1. `calculate_soft_delete_costs`
   * This function encapsulates the most intricate query, which concurrently retrieves two metrics:
      * `storage.googleapis.com/storage/v2/deleted_bytes`:  This metric quantifies the volume of data, in bytes, that has undergone soft deletion.
      * `storage.googleapis.com/storage/v2/total_byte_seconds`: This metric records the cumulative byte-seconds of data stored within the bucket, excluding objects marked for soft deletion.
   * Subsequently, the query computes the ratio of these two metrics, yielding the proportion of soft-deleted data relative to the total data volume within each bucket.
     
3. `get_storage_class_ratio`

   * This function employs a less complex query to re-acquire the  `storage.googleapis.com/storage/v2/total_byte_seconds` metric again.metric. However, in this instance, it focuses on segregating and aggregating the data based on the storage class associated with each object within the bucket.
   * The resultant output is a breakdown elucidating the distribution of data across various storage classes, facilitating a more granular cost analysis. For example, a result like `{ "bucket_name-STANDARD": 0.90, "bucket_name-NEARLINE": 0.10 }` indicates that the bucket's data is stored across two storage classes with a ratio of 9:1.

#### Key Formula

The relative increase in cost of using soft delete is calculated by combining the output of above mentioned queries and the for each bucket,

```
Relative cost of each bucket = ('deleted bytes' / 'total bytes seconds' )
                                 × 'soft delete retention duration'
                                 x 'cost of storing in storage class'
                                 x 'ratio of storage class'.
```

where,
   * `Soft Delete Retention Duration`: The number of days (or seconds) that soft-deleted objects are retained before permanent deletion. Longer retention periods increase potential costs.
   * `Deleted Bytes`: The amount of data (in bytes) that has been soft-deleted within the bucket.
   * `Total Bytes Seconds`: A cumulative measure of all data stored in the bucket (including active and soft-deleted objects) over time, expressed in byte-seconds (bytes * seconds).
   * `Cost of Storing in Storage Class`: The per-byte-second cost of the specific storage class where the soft-deleted data resides (e.g., Standard, Nearline, Coldline).
   * `Ratio of Storage Class`: The proportion of the bucket's data that belongs to the specific storage class being considered.

##### Explaination of each Steps:

1. Soft Delete Ratio: Divide `Deleted Bytes` by `Total Bytes Seconds` to get the fraction of data that is soft-deleted. This indicates how much of the overall storage is occupied by inactive, potentially deletable data.
2. Cost Impact:
   * Multiply the `Soft Delete Ratio` by the `Soft Delete Retention Duration` to account for the extra time this data is being stored.
   * Multiply this result by the 'Cost of Storing in Storage Class` to factor in the pricing of the specific storage class.
   * Finally, multiply by the `Ratio of Storage Class` to consider only the portion of the cost attributable to that particular class.

The final result represents the relative increase in cost due to soft delete, expressed as a fraction or percentage. A higher value indicates a more significant cost impact. This allows you to assess whether the benefits of soft delete (data protection) outweigh the additional storage expenses for each bucket and storage class. Example: If the calculated relative cost increase is 0.15 (or 15%), it means that enabling soft delete for that bucket/storage class would increase your storage costs by approximately 15%.



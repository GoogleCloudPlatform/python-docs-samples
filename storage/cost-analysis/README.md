Google Cloud Storage Python Samples
===============================================================================

[![Open in Cloud Shell button](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/s3-sdk/README.rst)

**Google Cloud Storage:** https://cloud.google.com/storage/docs 

Samples
-------------------------------------------------------------------------------
NOTE: Due to the specific functionality related to Google Cloud APIs, this guide assumes a base level of familiarity with Google Cloud Storage features, terminology, and pricing.

### Google Cloud Storage Soft Delete Cost Analyzer
-------------------------------------------------------------------------------
**Understanding Soft Delete and Cost Considerations**
   1. Soft Delete: A feature for protecting against accidental data loss. Deleted objects are retained for a defined period before permanent deletion. This adds safety but carries potential additional storage costs.
   2. Cost Analysis: This script evaluates the relative cost increase within each bucket if soft delete is enabled. Considerations include:
        * Your soft delete retention window
        * Amount of data likely to be soft-deleted
        * Proportions of data in different storage classes (e.g., Standard, Nearline)

**How to Use the Script**

**Prerequisites**

     1. A Google Cloud Platform (GCP) Project with existing buckets.
     2. Permissions on your GCP project to interact with Google Cloud Storage and Monitoring APIs.
     3. A Python environment (https://cloud.google.com/python/setup)

**Command-Line Arguments**
* `project_name` - (**Required**): Specifies your GCP project name.
* `--cost_threshold` - (Optional, default=0): Sets a relative cost threshold.
* `--soft_delete_window` - (Optional, default= 604800.0 (i.e. 7 days)): Time window (in seconds) for considering soft-deleted objects..
* `--agg_days` - (Optional, default=30): The period over which to combine and aggregate results.
* `--lookback_days` - (Optional, default=360): Time window (in days) for considering the how old the bucket to be.
* `--list` - (Optional, default=False): Produces a simple list of bucket names.

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

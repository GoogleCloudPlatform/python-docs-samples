
For requester_pays_test.py, we need to use a different Storage bucket.

The test looks for an environment variable
`REQUESTER_PAYS_TEST_BUCKET` first and then fallback to
`${CLOUD_STORAGE_BUCKET} + '-requester-pays-test'`.

On the test project, we created a bucket named
`python-docs-samples-tests-requester-pays-test`.


Also, the service account for the test needs to have `Billing Project
Manager` role in order to make changes on buckets with requester pays
enabled.

We added that role to the test service account.

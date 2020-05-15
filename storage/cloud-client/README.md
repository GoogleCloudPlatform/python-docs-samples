
For requester_pays_test.py, we need to use a different Storage bucket.

The test looks for an environment variable `REQUESTER_PAYS_TEST_BUCKET`.

Also, the service account for the test needs to have `Billing Project
Manager` role in order to make changes on buckets with requester pays
enabled.

We added that role to the test service account.

# How to set up/ tear down the test resources

## Required environment variables

To successfully import the catalog data for tests, the following environment variables should be set:
 - PROJECT_NUMBER
 - BUCKET_NAME
These values are stored in the Secret Manager and will be submitted as 
   docker environment variables before the test run.
   
The Secret Manager name is set in .kokoro/presubmit/common.cfg file, SECRET_MANAGER_KEYS variable.

## Import catalog data

There is a JSON file with valid products prepared in the `product` directory:
`resources/products.json`.

Run the `create_test_resources.py` to perform the following actions:
   - create the GCS bucket <BUCKET_NAME>, 
   - upload the product data from `resources/products.json` file,
   - import products to the default branch of the Retail catalog.

```
$ python create_test_resources.py
```

In the result 316 products should be created in the test project catalog.


## Remove catalog data

Run the `remove_test_resources.py` to perform the following actions:
   - remove all objects from the GCS bucket <BUCKET_NAME>, 
   - remove the <BUCKET_NAME> bucket,
   - delete all products from the Retail catalog.

```
$ python remove_test_resources.py
```
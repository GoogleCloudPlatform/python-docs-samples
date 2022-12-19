# How to set up/ tear down the test resources

## Required environment variables

To successfully import the catalog data for tests, the following environment variables should be set:
 - BUCKET_NAME
 - EVENTS_BUCKET_NAME
These values are stored in the Secret Manager and will be submitted as 
   docker environment variables before the test run.
   
The Secret Manager name is set in .kokoro/presubmit/common.cfg file, SECRET_MANAGER_KEYS variable.

## Import catalog data

There are JSON files with valid products and user events prepared in `resources` directory:
`samples/resources/products.json` and `samples/resources/user_events.json` respectively.

Run the `create_test_resources.py` to perform the following actions:
   - create the GCS bucket <BUCKET_NAME>, 
      - upload the product data from `resources/products.json` file to products bucket,
   - import products to the default branch of the Retail catalog,
   - create the GCS bucket <EVENTS_BUCKET_NAME>, 
      - upload the product data from `resources/user_events.json` file to events bucket,
   - create a BigQuery dataset and table `products`,
      - insert products from resources/products.json to the created products table,
   - create a BigQuery dataset and table `events`,
      - insert user events from resources/user_events.json to the created events table
  

```
$ python create_test_resources.py
```

In the result 316 products should be created in the test project catalog.


## Remove catalog data

Run the `remove_test_resources.py` to perform the following actions:
   - remove all objects from the GCS bucket <BUCKET_NAME>, 
   - remove the <BUCKET_NAME> bucket,
   - delete all products from the Retail catalog.
   - remove all objects from the GCS bucket <EVENTS_BUCKET_NAME>, 
   - remove the <EVENTS_BUCKET_NAME> bucket,
   - remove dataset `products` along with tables
   - remove dataset `user_events` along with tables 

```
$ python remove_test_resources.py
```
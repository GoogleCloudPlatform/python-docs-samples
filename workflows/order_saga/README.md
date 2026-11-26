# Compensate multi-step failures with a saga in Cloud Workflows

Across multiple services, a step can commit while a later step fails, or a step can time out after its side effect already happened. This sample coordinates a multi-step saga in Cloud Workflows where every forward and compensating step is idempotent, using an order charge, fulfillment, and refund as the example.

If charging exhausts its retries after an ambiguous timeout, or if fulfillment fails permanently, the workflow runs the compensating step to refund an existing charge or void the charge key so a late request cannot charge afterward.

## Deploy

Deploy `payment-provider` and `process-payment` using [`../idempotent_payment/README.md`](../idempotent_payment/README.md), then deploy the stand-in fulfillment service, the compensating refund function, and the saga workflow:

```sh
gcloud functions deploy fulfillment-service --gen2 --runtime=python313 \
  --region="$REGION" --source=../fulfillment_service --entry-point=fulfill \
  --trigger-http --no-allow-unauthenticated --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="FIRESTORE_DATABASE=$DATABASE" --project="$PROJECT_ID"

FULFILLMENT_URL=$(gcloud functions describe fulfillment-service --gen2 \
  --region="$REGION" --project="$PROJECT_ID" --format='value(serviceConfig.uri)')

gcloud functions deploy refund-order --gen2 --runtime=python313 \
  --region="$REGION" --source=. --entry-point=refund_order \
  --trigger-http --no-allow-unauthenticated --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="FIRESTORE_DATABASE=$DATABASE,PAYMENT_PROVIDER_URL=$PROVIDER_URL" \
  --project="$PROJECT_ID"

REFUND_URL=$(gcloud functions describe refund-order --gen2 \
  --region="$REGION" --project="$PROJECT_ID" --format='value(serviceConfig.uri)')

gcloud workflows deploy order-saga-workflow --source=workflow.yaml \
  --location="$REGION" --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="PAYMENT_FUNCTION_URL=$FUNCTION_URL,FULFILLMENT_URL=$FULFILLMENT_URL,REFUND_FUNCTION_URL=$REFUND_URL,FIRESTORE_DATABASE=$DATABASE" \
  --project="$PROJECT_ID"
```

## Test

```sh
pytest tests/main_test.py

RUN_INTEGRATION_TESTS=true GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \
  GOOGLE_CLOUD_LOCATION="$REGION" FIRESTORE_DATABASE="$DATABASE" \
  pytest tests/integration_test.py
```

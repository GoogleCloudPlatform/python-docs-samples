# Make HTTP calls idempotent from Cloud Workflows

When a workflow retries a timed-out HTTP call, or a client retries a workflow execution, neither caller knows whether the downstream service already ran. This sample pairs a Cloud Workflow with a Cloud Run function backed by Firestore so each request runs its side effect at most once, using an order payment as the example.

The workflow claims the request in Firestore by client-supplied ID (or resumes from the stored state on conflict), and the function holds a short lease while calling an external provider with an `Idempotency-Key` outside the transaction.

## Deploy

Set `PROJECT_ID`, `REGION`, `SERVICE_ACCOUNT` (needs `roles/datastore.user` and `roles/run.invoker`), and `DATABASE` (for example `(default)` for a Firestore Native database).

Deploy the stand-in payment provider first (in production, point `PAYMENT_PROVIDER_URL` at your provider's API instead):

```sh
gcloud functions deploy payment-provider --gen2 --runtime=python313 \
  --region="$REGION" --source=../payment_provider --entry-point=payment_provider \
  --trigger-http --no-allow-unauthenticated --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="FIRESTORE_DATABASE=$DATABASE" --project="$PROJECT_ID"

PROVIDER_URL=$(gcloud functions describe payment-provider --gen2 \
  --region="$REGION" --project="$PROJECT_ID" --format='value(serviceConfig.uri)')
```

Deploy the idempotent function and the workflow:

```sh
gcloud functions deploy process-payment --gen2 --runtime=python313 \
  --region="$REGION" --source=. --entry-point=process_payment \
  --trigger-http --no-allow-unauthenticated --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="FIRESTORE_DATABASE=$DATABASE,PAYMENT_PROVIDER_URL=$PROVIDER_URL" \
  --project="$PROJECT_ID"

FUNCTION_URL=$(gcloud functions describe process-payment --gen2 \
  --region="$REGION" --project="$PROJECT_ID" --format='value(serviceConfig.uri)')

gcloud workflows deploy idempotent-order-workflow --source=workflow.yaml \
  --location="$REGION" --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="PAYMENT_FUNCTION_URL=$FUNCTION_URL,FIRESTORE_DATABASE=$DATABASE" \
  --project="$PROJECT_ID"
```

## Test

```sh
pytest tests/main_test.py

RUN_INTEGRATION_TESTS=true GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \
  GOOGLE_CLOUD_LOCATION="$REGION" FIRESTORE_DATABASE="$DATABASE" \
  pytest tests/integration_test.py
```

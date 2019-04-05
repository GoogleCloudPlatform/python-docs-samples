# Log Sink Throttling

CLI used to throttle messages from Audit Log to SCC.

## How to use it

```bash
(cd cli; \
pipenv run python3 log_sink_throttling.py \
--project ${scc_logs_project_id} \
--subscription "log_sink_throttling_subscription" \
--forward-topic "log_sink" \
--sleep-seconds 2 \
--no-print-messages;)
```

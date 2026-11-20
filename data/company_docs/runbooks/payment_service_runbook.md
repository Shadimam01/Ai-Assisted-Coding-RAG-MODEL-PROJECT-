# Payment Service Runbook

## Symptom: Payment gateway timeout (HTTP 503 / ConnectionTimeout)
Likely causes: gateway outage, exhausted connection pool, or network issue.
Steps:
1. Check the gateway status page and the #payments-alerts channel.
2. Check the connection pool usage on the Payment Service dashboard. If above 90 percent, restart the service pod.
3. Retry failed payments using the original Idempotency-Key. Never create a new key for a retry.
4. If timeouts last more than 15 minutes, escalate to the on-call payments engineer.

## Symptom: HTTP 401 Unauthorized from Payment API
Cause: expired or missing token. Request a new token from /auth/token and retry.
If it keeps happening, check that the server clock is synced (NTP).

## Symptom: HTTP 429 Too Many Requests
Cause: rate limit of 100 requests per minute exceeded.
Fix: add exponential backoff with retries (1s, 2s, 4s) and reduce parallel requests.

## Symptom: Database connection pool exhausted
Cause: connections not released, or traffic spike.
Fix: ensure connections are closed in a finally block, then increase pool size from 20 to 40 in config if load requires.

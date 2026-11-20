# Payment API Guide (Acme Corp)

## Authentication
All requests to the Payment API must include a Bearer token in the Authorization header.
Tokens expire after 60 minutes. A 401 response means the token is missing or expired; request a new token from /auth/token.

## Create a payment
POST /v2/payments
Required fields: amount (integer, in paise), currency (ISO code), customer_id.
Every request must include an Idempotency-Key header to prevent duplicate charges.

## Rate limits
The API allows 100 requests per minute per client. Exceeding this returns HTTP 429.
Clients must retry with exponential backoff: wait 1s, 2s, 4s, up to 5 attempts.

## Error codes
- 400: Invalid request body.
- 401: Missing or expired token.
- 402: Payment declined by the bank.
- 429: Rate limit exceeded.
- 503: Payment gateway timeout. Safe to retry using the same Idempotency-Key.

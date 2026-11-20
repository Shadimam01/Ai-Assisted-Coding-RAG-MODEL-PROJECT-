# Acme Corp Coding Standards

## Naming
- REST endpoints use lowercase plural nouns with hyphens, e.g. /user-accounts. No verbs in paths.
- Python functions and variables use snake_case. Classes use PascalCase.
- Constants use UPPER_SNAKE_CASE.

## Error handling
- Never use a bare "except:". Catch specific exceptions.
- Every external call (HTTP, database) must have a timeout.
- Log errors with a correlation ID. Never log passwords, tokens or card numbers.

## Security
- Secrets must come from environment variables, never from source code.
- All user input must be validated before use.

## Code review
- Every pull request needs at least one approval and passing tests.
- Functions longer than 50 lines should be split.

# Security Considerations

This is an educational/local MVP.

## Current Practices
- `.env` is excluded from Git.
- API inputs are validated.
- Watering checks device and pump state.
- Tank refill is prevented while the pump is running.

## Never Commit

```text
.env
API keys
Passwords
Private tokens
Cloud credentials
Database credentials
```

## Production Requirements

A production deployment should add:
- Authentication
- Authorization
- HTTPS
- Secure secret storage
- Device credentials
- Token rotation
- API rate limiting
- Audit logs
- Database backups
- Monitoring

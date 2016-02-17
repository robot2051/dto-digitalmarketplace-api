## Cloud Foundry steps thus far
```
cf target -o digital-marketplace -s dev
cf push digitalmarkteplace-api --no-start
cf set-env digitalmarketplace-api DM_ENVIRONMENT preview
cf set-env digitalmarketplace-api DEBUG 1
cf set-env digitalmarketplace-api DM_API_AUTH_TOKENS somedummytoken
cf create-service PostgreSQL "Basic PostgreSQL Plan" digitalmarketplace_api_db
cf bind-service digitalmarketplace-api digitalmarketplace_api_db
cf push digitalmarketplace-api -c 'python application.py db upgrade' -i 1
cf push digitalmarketplace-api
```

## Next steps
- Move DB migration to startup. This is what cloudfoundry suggest [1].

[1] https://docs.cloudfoundry.org/devguide/services/migrate-db.html#frequent-migration

# Hotels API

## CSV Data Import

To import CSV data into a database table, use the following command (specific to PostgreSQL):

```postgresql
COPY table_name FROM '/absolute/path/to/your/file.csv' DELIMITER ',' CSV HEADER;
```

For more details, see the [PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-copy.html).

## SMTP Server

Use [MailHog](https://github.com/mailhog/MailHog) to start a local SMTP server and test email functionality.

## Direnv

If you use the [direnv](https://direnv.net/) utility to load `.env` variables into your environment, remember to disable
it during testing. This is because [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
prioritizes environment variables first, and only then loads variables from the env files (in our case
from `.env.test`).

## Testing in PyCharm

To ensure that `pydantic-settings` can locate the `.env.test` file in the root directory during tests run from the IDE,
you need to specify the path to it in the **Run Configuration**.

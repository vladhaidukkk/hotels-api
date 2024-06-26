# Hotels API

## CSV Data Import

To import CSV data into a database table, use the following command (specific to PostgreSQL):

```postgresql
COPY table_name FROM '/absolute/path/to/your/file.csv' DELIMITER ',' CSV HEADER;
```

For more details, see the [PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-copy.html).

## SMTP Server

Use [MailHog](https://github.com/mailhog/MailHog) to start a local SMTP server and test email functionality.

# Hotels API

## CSV Data Import

To import CSV data into a database table, use the following command (specific to PostgreSQL):

```postgresql
COPY table_name FROM '/absolute/path/to/your/file.csv' DELIMITER ',' CSV HEADER;
```

For more details, see the [PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-copy.html).

## SMTP Server

Use [MailHog](https://github.com/mailhog/MailHog) to start a local SMTP server and test email functionality.

## Testing in PyCharm

To ensure that `pydantic-settings` can locate the `.env` file in the root directory during tests run from the IDE, you
need to specify the path to it in the **Run Configuration**.

## Docker Compose

In the `docker/app.sh` file, you can find two commands that run when executing `docker compose up` to start the web app
service. In most cases, the migrations fail on the initial run, so don't worry and run them twice.

## Grafana

To set up a Grafana dashboard, you first need to create a data source for Prometheus. Then, replace the `uid` field in
the `grafana-dashboard.json` file with the UID of this data source. Finally, create the dashboard using the provided
JSON file.

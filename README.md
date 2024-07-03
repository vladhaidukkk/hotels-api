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

## Hosting

### Render Platform

[Render](https://dashboard.render.com/) is a platform used to host PostgreSQL databases, Redis instances, and web
services. It provides an easy-to-use, yet limited, solution for small applications. For demonstration purposes, it is an
ideal option.

The hosted web service for this FastAPI application is available at https://hotels-api-e2zy.onrender.com. Please note
that this service will only be active for one month from the date of deployment, so it should not be accessible after
03.08.2024.

#### Migrations on Render

To run migrations on the database instance of Render, simply connect to it locally and execute the migrations.

### Virtual Private Server (VPS)

A VPS is a more flexible option for hosting your application. To set it up, follow these steps:

1. Rent a VPS.
2. Optionally, purchase a domain.
3. Connect to the VPS via SSH.
4. Install Git and Docker on the VPS.
5. Clone the repository on the VPS.
6. Create the `.env` and `.env.prod` files on the VPS.
7. Correct the `nginx.conf` file if necessary.
8. Run `docker compose build` to build the web app image.
9. Run `docker compose up` to start all the services.
10. Add an SSL certificate if you require HTTPS.

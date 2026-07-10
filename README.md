# Registration UI
This is a small tool to handle our project-registrations. Feel free to adapt it to your needs!

## Installation
### Production
Intended for use with reverse proxy (port: 1337)!
- Create `projectSecrets.py` and `.env` by copying the templates
- Fill in all values in `projectSecrets.py` and `.env`
    - DJANGO_ALLOWED_HOSTS are separated by spaces
    - create KEY through: ```py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"```
- ```docker-compose up -d --build```

Security-sensitive settings can be supplied through the environment instead of
`projectSecrets.py`: `DJANGO_SECRET_KEY`, `EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_SSL`, and `EMAIL_USE_TLS`.
Production defaults to HTTPS redirects and one year of HSTS; set
`DJANGO_SECURE_SSL_REDIRECT=False` only when TLS termination is not used.

> **Database upgrade:** the Compose image now uses PostgreSQL 16. Before starting
> it against an existing PostgreSQL 12 volume, export the database with `pg_dump`
> and restore it into a fresh PostgreSQL 16 volume. PostgreSQL data directories
> cannot be reused across major versions.

The included migration helper performs this upgrade offline, retains both an
SQL dump and a copy of the original PostgreSQL 12 volume, and then runs Django
migrations:

```sh
chmod +x scripts/migrate-postgres-12-to-16.sh
./scripts/migrate-postgres-12-to-16.sh
```

Run it from the repository root on the Docker host. Expect downtime while the
database is copied and restored. Do not delete the reported backup volume or
SQL dump until the upgraded deployment has been verified.
### Development
- Install requirements: ```pip install -r requirements.txt```
- Initialize DB: ```python manage.py migrate```
- Start local server: ```python ./manage.py runserver```


## Infos
- The website is based on Bootstrap

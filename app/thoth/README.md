[Русский](README_ru.md)

## Thoth: Bitrix24 Integration Hub 

### Description

One Thoth installation allows you to create and manage an unlimited number of local and mass-distributed Bitrix24 applications with OAuth 2.0 authorization.

## Video Instructions on YouTube

https://www.youtube.com/playlist?list=PLeniNJl73vVmmsG1XzTlimbZJf969LIpS

## Installation

+ Python 3.12
+ PostgreSQL 16
+ Redis

```
cd /opt git clone https://github.com/vaestvita/thoth cd thoth

python3 -m venv .venv source .venv/bin/activate pip install -r requirements/production.txt

cp docs/example/env_example .env nano .env replace ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS with your values 
Replace the value of DATABASE_URL with your own (the psql database must be created beforehand)

python manage.py migrate 
python manage.py collectstatic 
python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000 (for testing and debugging)
```


The default path to access the admin panel is /admin. To set your own path, change the DJANGO_ADMIN_URL variable in the .env file.

## Database
The [DJ-Database-URL](https://github.com/jazzband/dj-database-url?tab=readme-ov-file#url-schema) module allows connecting various databases. See the documentation via the link.

## Update

```
cd /opt/thoth
source .venv/bin/activate
git pull
python manage.py migrate
systemctl restart thoth
```


## Proxy Server
+ You can view the process of setting up Nginx and Gunicorn [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)
+ Example configuration files are available in the [documentation](docs/example)

## Logging
If needed, you can enable detailed logs in the console. To do this, specify the logging level LOG_LEVEL=DEBUG in the .env file, restart thoth, and run the command

```
journalctl -u thoth -f
```


## Integration

+ [Bitrix24 CRM](docs/bitrix.md)
+ [(WhatsApp) WABA](docs/waba.md)
+ [OLX](docs/olx.md)

docker exec -it cont-center python /app/thoth/manage.py migrate
docker exec -it cont-center python /app/thoth/manage.py collectstatic
docker exec -it cont-center python /app/thoth/manage.py createsuperuser

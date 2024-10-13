# Eliminar cache docker
docker system prune -a -f

# Requirements
```
pip freeze > requirements.txt
```

# Crear tablas
```
 docker exec -it $service flask db init
 docker exec -it $service flask db migrate
 docker exec -it $service flask db upgrade
```

# Por si no se borran migraciones viejas
```
docker exec -it app-e-comercio-main-db-1 psql -U main_app_user -d main_app_db

DROP TABLE catalogo_schema.alembic_version;
\q

docker exec -it app-e-comercio-main-ms_catalogo-1 flask db stamp head

docker exec -it app-e-comercio-main-ms_catalogo-1 flask db migrate -m "Initial migration for catalogo"
docker exec -it app-e-comercio-main-ms_catalogo-1 flask db upgrade

```

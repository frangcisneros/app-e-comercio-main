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

# Recrear imagenes docker
docker compose pull to check for and if available pull a new image

docker compose down to shut down the current container (optional)

docker compose up -d to start a new container using the compose config and the new pulled image.
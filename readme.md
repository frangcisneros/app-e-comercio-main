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
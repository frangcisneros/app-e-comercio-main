#!/bin/bash
#EJECUTAR CON TERMINAL GIT BASH

services=("app-e-comercio-main-ms_compras-1" "app-e-comercio-main-ms_stock-1" "app-e-comercio-main-ms_catalogo-1" "app-e-comercio-main-ms_pago-1")
database="main_app_dev_db"

echo "Inicializando migraciones para la base de datos $database"
docker exec -it db psql -U main_app_user -d $database -c "CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)"

for service in "${services[@]}"
do
  echo "Verificando estado de migraciones para $service en $database"
  docker exec -it $service bash -c "export DATABASE_URL=postgresql+psycopg2://main_app_user:main_app_password@db:5432/$database && flask db current"

  echo "Ejecutando migraciones para $service en $database"
  docker exec -it $service bash -c "export DATABASE_URL=postgresql+psycopg2://main_app_user:main_app_password@db:5432/$database && flask db upgrade" || {
    echo "Error ejecutando migraciones para $service en $database"
    exit 1  # Salir del script si ocurre un error
  }
done
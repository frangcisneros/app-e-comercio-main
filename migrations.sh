#!/bin/bash
#EJECUTAR CON TERMINAL GIT BASH

services=("ms_compras" "ms_stock" "ms_catalogo" "ms_pago")
databases=("main_app_dev_db" "main_app_test_db" "main_app_prod_db")

for db in "${databases[@]}"
do
  echo "Inicializando migraciones para la base de datos $db"
  docker exec -it db psql -U main_app_user -d $db -c "CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)"
  for service in "${services[@]}"
  do
    echo "Ejecutando migraciones para $service en $db"
    docker exec -it $service bash -c "export DATABASE_URL=postgresql+psycopg2://main_app_user:main_app_password@db:5432/$db && flask db upgrade"
  done
done
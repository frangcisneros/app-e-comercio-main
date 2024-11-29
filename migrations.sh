#!/bin/bash
#EJECUTAR CON TERMINAL GIT BASH

services=("ms_compras" "ms_stock" "ms_catalogo" "ms_pago")

for service in "${services[@]}"
do
  echo "Inicializando base de datos para $service"
  docker exec -it $service flask db init
  docker exec -it $service flask db migrate
  docker exec -it $service flask db upgrade
done
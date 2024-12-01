services=("ms_compras" "ms_stock" "ms_catalogo" "ms_pago")
databases=("main_app_dev_db" "main_app_test_db" "main_app_prod_db")

for service in "${services[@]}"

do
  echo "Inicializando base de datos para $service"
  docker exec -it $service flask db init
  docker exec -it $service flask db migrate
  docker exec -it $service flask db upgrade
done
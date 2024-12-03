services=("app-e-comercio-main-ms_compras-1" "app-e-comercio-main-ms_stock-1" "app-e-comercio-main-ms_catalogo-1" "app-e-comercio-main-ms_pago-1")
databases=("main_app_dev_db" "main_app_test_db" "main_app_prod_db")

for service in "${services[@]}"

do
  echo "Inicializando base de datos para $service"
  docker exec -it $service flask db init
  docker exec -it $service flask db migrate
  docker exec -it $service flask db upgrade
done
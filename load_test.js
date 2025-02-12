import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
	stages: [
		{ duration: '1s', target: 60 }, 
		{ duration: '3m', target: 60 }, 
	],
	hosts: {
		'ecommerce.universidad.localhost': '127.0.0.1',
		'stock.universidad.localhost': '127.0.0.1'
	},
	insecureSkipTLSVerify: true,
};

export function setup() {
	// Llenar la tabla de stock con 100 unidades de un producto
	let refuelRes = http.post(
		"http://stock.universidad.localhost/api/v1/stock/refuel",
		JSON.stringify({ product_id: 2, quantity: 100 }),
		{
			headers: { "Content-Type": "application/json" },
		}
	);
	check(refuelRes, { "status was 200": (r) => r.status === 200 });
}

export default function () {
	// Realizar la solicitud de venta utilizando saga_compra
	let data = {
		producto_id: 2,
		product_id: 2,
		direccion_envio: "Calle Falsa 123",
		precio: 100,
		medio_pago: "tarjeta",
		quantity: 2,
	};

	let sellRes = http.post(
		"http://ecommerce.universidad.localhost/api/v1/saga/compra",
		JSON.stringify(data),
		{
			headers: { "Content-Type": "application/json" },
		}
	);
	check(sellRes, { "status was 200": (r) => r.status === 200 });

	// Chequear la cantidad de stock después de cada venta
	let checkRes = http.get(
		"http://stock.universidad.localhost/api/v1/stock/check_quantity/2"
	);
	check(checkRes, { "status was 200": (r) => r.status === 200 });
	console.log(
		`Stock quantity after ${__ITER + 1} iterations: ${checkRes.json().quantity}`
	);

	sleep(1);
}

export function teardown() {
	// Eliminar todos los productos del stock
	let getAllRes = http.get("http://stock.universidad.localhost/api/v1/stock/get_all");
	check(getAllRes, { "status was 200": (r) => r.status === 200 });
	let products = getAllRes.json();
	products.forEach((product) => {
		let deleteRes = http.del(
			`http://stock.universidad.localhost/api/v1/stock/delete_product/${product.product_id}`
		);
		check(deleteRes, { "status was 200": (r) => r.status === 200 });
	});
	console.log("Stock table has been cleared.");
}

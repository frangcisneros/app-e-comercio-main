-- init-db.sql

CREATE DATABASE main_app_dev_db;
CREATE DATABASE main_app_prod_db;

-- Conectar a la base de datos principal
\c main_app_db;

-- Crear los esquemas para cada microservicio
CREATE SCHEMA IF NOT EXISTS stock_schema;
CREATE SCHEMA IF NOT EXISTS compras_schema;
CREATE SCHEMA IF NOT EXISTS pago_schema;
CREATE SCHEMA IF NOT EXISTS catalogo_schema;

-- Conectar a la base de datos principal
\c main_app_test_db;

-- Crear los esquemas para cada microservicio
CREATE SCHEMA IF NOT EXISTS stock_schema;
CREATE SCHEMA IF NOT EXISTS compras_schema;
CREATE SCHEMA IF NOT EXISTS pago_schema;
CREATE SCHEMA IF NOT EXISTS catalogo_schema;

-- Conectar a la base de datos principal
\c main_app_prod_db;

-- Crear los esquemas para cada microservicio
CREATE SCHEMA IF NOT EXISTS stock_schema;
CREATE SCHEMA IF NOT EXISTS compras_schema;
CREATE SCHEMA IF NOT EXISTS pago_schema;
CREATE SCHEMA IF NOT EXISTS catalogo_schema;
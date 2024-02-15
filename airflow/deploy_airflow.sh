#!/bin/bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
AIRFLOW_UID=50000
# initial airflow
docker compose up airflow-init
# run airflow container
docker compose up -d
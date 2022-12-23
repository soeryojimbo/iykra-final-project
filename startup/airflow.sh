#!/bin/bash

echo "Changing permissions for dbt folder..."
cd ~/OnlinePaymentFraud-LambdaArchitecture/ && sudo chmod -R 777 dbt

echo "Change Airflow folder owner on dags logs and plugin..."
cd ~/OnlinePaymentFraud-LambdaArchitecture/airflow && sudo chown -R $USER:$USER dags \
&& sudo chown -R $USER:$USER logs \
&& sudo chown -R $USER:$USER plugins

echo "Building airflow docker images..."
cd ~/OnlinePaymentFraud-LambdaArchitecture/airflow
docker compose build

echo "Running airflow-init..."
docker compose up airflow-init

echo "Starting up airflow in detached mode..."
docker compose up -d

echo "Airflow started successfully."
echo "Airflow is running in detached mode. "
echo "Run 'docker-compose logs --follow' to see the logs."
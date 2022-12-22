from datetime import datetime
from airflow.providers.google.cloud.operators.bigquery import (BigQueryCreateEmptyDatasetOperator,
                                                               BigQueryDeleteTableOperator)
from airflow import DAG
from airflow.operators.bash import BashOperator
import os

target_dataset = "onlinepayment_prod"
PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", target_dataset)
tabletodelete = "stg_onlinepayment"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id = 'transform_dbt',
    default_args = default_args,
    description = 'Test dbt',
    schedule_interval="@once",
    start_date=datetime(2022,3,20),
    catchup=True,
    tags=['dbt']

) as dag:

    create_dataset_task = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset_task",
        dataset_id=target_dataset,
        location="US",
    )
    initiate_staging_task = BashOperator(
        task_id = "initiate_staging_task",
        bash_command = "cd /dbt && dbt deps && dbt run --select stg_onlinepayment --profiles-dir . --target prod"
    )
    transform_task = BashOperator(
        task_id = "transform_task",
        bash_command = "cd /dbt && dbt deps && dbt run --exclude stg_onlinepayment --profiles-dir . --target prod"
    )
    delete_staging_table_task = BigQueryDeleteTableOperator(
        task_id = "delete_staging_table_task",
        deletion_dataset_table = f'{PROJECT_ID}.{BIGQUERY_DATASET}.{tabletodelete}',
        ignore_if_missing = True
    )
    create_dataset_task >> initiate_staging_task >> transform_task >> delete_staging_table_task
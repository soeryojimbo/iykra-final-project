import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import (BigQueryCreateExternalTableOperator,
                                                               BigQueryCreateEmptyDatasetOperator)

from datetime import datetime
from google.cloud import storage
import pyarrow.csv as pv
import pyarrow.parquet as pq

# PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
# BUCKET = os.environ.get("GCP_GCS_BUCKET")
PROJECT_ID = "iykra-fahmi"
BUCKET = "final_project_group_4"


dataset_file = "PS_20174392719_1491204439457_log.csv"
parquet_file = dataset_file.replace('.csv', '.parquet')
dataset_url = f"https://media.githubusercontent.com/media/fahmihamzah84/fraud_log_file/master/{dataset_file}"
# path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
path_to_local_home = "/opt/airflow/"
downloaded_csv = f'{path_to_local_home}/{dataset_file}'
downloaded_parquet = f'{path_to_local_home}/{parquet_file}'
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "onlinepayment_stg")
staging_dataset = "onlinepayment_stg"

def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="ingest_data",
    start_date= datetime(2022,12,23),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['Online_payment'],
) as dag:
    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSL {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )

    remove_files_from_local_task=BashOperator(
        task_id='remove_files_from_local',
        bash_command=f'rm {downloaded_csv} {downloaded_parquet}'
    )

    create_dataset_task = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset_task",
        dataset_id=staging_dataset,
        location="US",
        )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id = f'bigquery_external_table_task',
        table_resource = {
            'tableReference': {
            'projectId': PROJECT_ID,
            'datasetId': BIGQUERY_DATASET,
            'tableId': 'online_payment_view',
            },
            'externalDataConfiguration': {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{parquet_file}"],
                "autodetect": True
            },
        },
    )

    download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> remove_files_from_local_task >> create_dataset_task >> bigquery_external_table_task

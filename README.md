# Online Fraud - Lambda Architecture

## Description
Online payment systems have helped many people to make payments instantly. But on the other hand, it also increases payment fraud. That is why detecting online payment fraud is very important for financial technology companies to ensure that customers are not getting charged for the products and services they never pay. 

So as data engineers, we need to build a data engineering infrastructure to turn raw data into dashboards that can later be used to see the company's transactions data health. 


### Objective
- Design and build end to end data pipeline.
- Created Dashboard to check the healthy transaction data.
- Check Transaction Healthy or Not


### Dataset
We use the online payment fraud system dataset on Kaggle. This dataset can be accessed on https://www.kaggle.com/datasets/rupakroy/online-payments-fraud-detection-dataset 

### Tools stack

- Cloud - [**Google Cloud Platform**](https://cloud.google.com)
- Virtualization or Containerization - [**Docker**](https://www.docker.com), [**Docker Compose**](https://docs.docker.com/compose/)
- Orchestration - [**Airflow**](https://airflow.apache.org)
- Transformation - [**dbt**](https://www.getdbt.com)
- Stream Processing - [**Google Pub/Sub**](https://cloud.google.com/pubsub/?utm_source=google&utm_medium=cpc&utm_campaign=japac-ID-all-en-dr-bkws-all-all-trial-e-dr-1009882&utm_content=text-ad-none-none-DEV_c-CRE_468709682064-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt%20~%20Data%20Analytics%20~%20Pub%2FSub_Cloud%20PubSub-KWID_43700029830238360-aud-1596662389134%3Akwd-395094646964&userloc_9072606-network_g&utm_term=KW_google%20pub%20sub&gclid=CjwKCAiAnZCdBhBmEiwA8nDQxcmEZPls8DLR-DwhIw2RG5_a8JJJpsdCM12Q6HJNZDZTMkE1oPB_dRoCpccQAvD_BwE&gclsrc=aw.ds)
- Data Lake - [**Google Cloud Storage**](https://cloud.google.com/storage)
- Data Warehouse - [**BigQuery**](https://cloud.google.com/bigquery)
- Data Visualization - [**Data Studio**](https://datastudio.google.com/overview)
- Language - [**Python**](https://www.python.org)

### Architecture
#### Batch Architecture
![Data_Streaming](https://user-images.githubusercontent.com/83212789/209272508-59dbf8d0-61ae-4d1d-9ccc-72b7a70f2d82.png)

#### Stream Architecture
![Data_Streaming drawio](https://user-images.githubusercontent.com/83212789/209273097-026dcb7b-a070-470a-bbdb-474c23a8e490.png)

### Result
The result of this end to end data pipeline project is the dashboard to check if the transaction was healthy or not.
You can check our dashboard in this link below:

https://datastudio.google.com/reporting/85df6c5e-d1ba-4bbf-a5ef-8cce3aa15422


<img width="764" alt="Dashboard" src="https://user-images.githubusercontent.com/83212789/209299445-bca44f9c-5573-47eb-bf26-b79d86be1c14.png">

## Setup
WARNING: You will be responsible for paying for all infrastructure setup. You can get $300 in credit by opening a new GCP account.

### Pre-requisites

If you already have a Google Cloud account and docker installed, you can skip the pre-requisite steps.

- Google Cloud Platform. 
  - [GCP Account and Access Setup](setup/gcp.md)
  - [gcloud alternate installation method - Windows](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/windows.md#google-cloud-sdk)

- After GCP account created, you can create a [new instances](https://cloud.google.com/compute/docs/instances/create-start-instance) 
and I suggest to use ubuntu boot disk.
- Docker setup on Ubuntu.
  - [Docker Setup](startup/docker.md)


### How to run

- Airflow & dbt - [Setup](airflow/README.md)
- Google Pub/Sub - [Setup](setup/pubsub.md)


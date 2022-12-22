{{ config(materialized="view") }}

select 
    md5(step || date || nameOrig || nameDest || type || amount) as transaction_id,
    CAST(date AS datetime) AS timestamp,
    CAST(step AS numeric) AS step,
    nameOrig AS IdSender,
    CAST(amount AS numeric) AS Amount,
    {{payment_type_desc ('type') }} AS type_id,
    CAST(oldbalanceOrg AS numeric) AS PrevBalanceSender,
    CAST(newbalanceOrig AS numeric) AS NewBalanceSender,
    nameDest AS IdReceiver,
    CAST(oldbalanceDest AS numeric) AS PrevBalanceReceiver,
    CAST(newbalanceDest	 AS numeric) AS NewBalanceReceiver,
    CAST(isFraud AS integer) AS Fraud,
    CAST(isFlaggedFraud AS integer) AS FlaggedFraud

from {{ source("staging", "online_payment_view") }}



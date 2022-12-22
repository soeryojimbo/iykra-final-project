{{ config(materialized="table") }}

SELECT
    IdSender,
    COUNT(IdSender) AS total_trx,
    Fraud,
    ARRAY_AGG(STRUCT(transaction_id,
            NewBalanceSender - PrevBalanceSender AS BalanceDiff)) AS trx

FROM 
    {{ref ('stg_onlinepayment')}}
GROUP BY 
    IdSender,
    Fraud
ORDER BY 
    total_trx desc, Fraud desc
{{ config(materialized="table") }}

SELECT
    IdReceiver,
    COUNT(IdReceiver) AS total_trx,
    Fraud,
    ARRAY_AGG(STRUCT(transaction_id,
            NewBalanceReceiver - PrevBalanceReceiver AS BalanceDiff)) AS trx

FROM 
    {{ref ('stg_onlinepayment')}}
GROUP BY 
    IdReceiver,
    Fraud
ORDER BY 
    total_trx desc, Fraud desc
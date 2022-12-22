
{{config (materialized="table") }}

SELECT
    transaction_id,
    timestamp,
    IdSender,
    Amount,
    IdReceiver,
    Fraud,
    type_id

FROM {{ref ('stg_onlinepayment')}}
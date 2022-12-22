{{config(materialized="table")}}

SELECT 
    DISTINCT(type_id) AS id,
    CASE
        WHEN type_id =  1 then 'PAYMENT'
        when type_id =  2 then 'CASH_OUT'
        when type_id =  3 then 'CASH_IN'
        when type_id =  4 then 'TRANSFER'
        when type_id =  5 then 'DEBIT'
    end AS payment_type

FROM {{ref ('stg_onlinepayment')}}
{{ config(
  materialized = 'table',
  partition_by={
    "field": "date",
    "data_type": "timestamp",
    "granularity": "day"}
    ) 
}}
with sender AS(
    SELECT IdSender, total_trx, 
    t.transaction_id as transaction_id, 
    t.BalanceDiff as BalanceDiff
FROM {{ref ('dim_sender') }},
UNNEST(trx) as t
),
receiver AS (
    SELECT IdReceiver, total_trx, 
    t.transaction_id as transaction_id, 
    t.BalanceDiff AS BalanceDiff
FROM {{ref ('dim_receiver') }},
UNNEST(trx) as t
)

SELECT
    fraudData.transaction_id AS transaction_id,
    fraudData.timestamp AS date,
    payment.payment_type,
    fraudData.IdSender AS IdSender,
    sender.total_trx AS CountTrxAsSender,
    fraudData.Amount AS AmountOfTrx,
    online_payment.PrevBalanceSender AS PrevBalanceSender,
    online_payment.NewBalanceSender AS NewBalanceSender,
    sender.BalanceDiff AS SendBalanceDiff,
    fraudData.IdReceiver AS IdReceiver,
    receiver.total_trx AS CountTrxAsRcv,
    online_payment.PrevBalanceReceiver AS PrevBalanceReceiver,
    online_payment.NewBalanceReceiver AS NewBalanceReceiver,
    receiver.BalanceDiff AS RcvBalanceDiff,
    fraudData.Fraud

FROM {{ref ('dim_fraud')}} AS fraudData
LEFT JOIN {{ref ('online_payment')}} AS online_payment
    ON fraudData.transaction_id = online_payment.transaction_id
LEFT JOIN {{ref ('dim_type_transaction')}} AS payment
    ON fraudData.type_id = payment.id
LEFT JOIN sender
    ON fraudData.transaction_id = sender.transaction_id
LEFT JOIN receiver
    ON fraudData.transaction_id = receiver.transaction_id

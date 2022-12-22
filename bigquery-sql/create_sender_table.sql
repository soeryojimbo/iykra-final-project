-- Create sender_table:
CREATE OR REPLACE TABLE `suryo-df8.final_project.sender_table`
AS
SELECT senderID, count(senderID) as count_trx,
  ARRAY_AGG(STRUCT(datetime, type, amount, oldbalanceSend, newbalanceSend,(newbalanceSend-oldbalanceSend) as difsender, isFraud) ORDER BY datetime) AS trx_detail
  from `suryo-df8.final_project.fraud_dataset_final`
  GROUP BY senderID
  order by count_trx desc;

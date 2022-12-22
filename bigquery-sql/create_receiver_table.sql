-- Create receiver table:
CREATE OR REPLACE TABLE `suryo-df8.final_project.receiver_table`
AS
SELECT ReceiverID, count(ReceiverID) as count_trx,
  ARRAY_AGG(STRUCT(datetime, type, amount, oldbalancereceive, newbalancereceive,(newbalancereceive-oldbalancereceive) as difreceiver, isFraud) ORDER BY datetime) AS trx_detail
  from `suryo-df8.final_project.fraud_dataset_final`
  GROUP BY ReceiverID
  order by count_trx desc;
